from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from faiss_index import FaissIndex

blueprint = Blueprint('faiss_index', __name__)

@blueprint.record_once
def record(setup_state):
    manage_faiss_index(
        setup_state.app.config.get('GET_FAISS_RESOURCES'),
        setup_state.app.config['GET_FAISS_INDEX'],
        setup_state.app.config['GET_FAISS_IDS_VECTORS'],
        setup_state.app.config.get('UPDATE_FAISS_AFTER_SECONDS'))

@blueprint.route('/faiss/search', methods=['POST'])
def search():
    try:
        json = request.get_json(force=True)
        validate(json, {
            'type': 'object',
            'required': ['k'],
            'properties': {
                'k': { 'type': 'integer', 'minimum': 1 },
                'ids': { 'type': 'array', 'items': { 'type': 'number' }},
                'vectors': {
                    'type': 'array',
                    'items': {
                        'type': 'array',
                        'items': { 'type': 'number' }
                    }
                }
            }
        })

        results_ids = blueprint.faiss_index.search_by_ids(json['ids'], json['k']) if 'ids' in json else []
        results_vectors = blueprint.faiss_index.search_by_vectors(json['vectors'], json['k']) if 'vectors' in json else []

        return jsonify(results_ids + results_vectors)

    except (BadRequest, ValidationError) as e:
        print("Bad Request", e)
        return "Bad Request", 400

    except Exception as e:
        print("Server error", e)
        return "Server error", 500

def manage_faiss_index(get_faiss_resources, get_faiss_index, get_faiss_ids_vectors, update_after_seconds):

    SIGNAL_SET_FAISS_INDEX = 1001
    SIGNAL_SET_FAISS_RESOURCES = 1002

    def set_faiss_index(*args):
        blueprint.faiss_index = FaissIndex(get_faiss_index(), get_faiss_ids_vectors())

    def set_faiss_resources(*args):
        get_faiss_resources()
        uwsgi.signal(SIGNAL_SET_FAISS_INDEX)

    def set_periodically():
        try:
            import uwsgi

            uwsgi.register_signal(SIGNAL_SET_FAISS_INDEX, 'workers', set_faiss_index)

            if get_faiss_resources:
                uwsgi.register_signal(SIGNAL_SET_FAISS_RESOURCES, 'worker', set_faiss_resources)
                uwsgi.add_timer(SIGNAL_SET_FAISS_RESOURCES, update_after_seconds)
            else:
                uwsgi.add_timer(SIGNAL_SET_FAISS_INDEX, update_after_seconds)

        except ImportError:
            print('Failed to load python module uwsgi')
            print('Periodic faiss index updates isn\'t enabled')
        except Exception:
            print('Failed to set periodic faiss index updates')
            print('UPDATE_FAISS_AFTER_SECONDS must be an integer')

    if update_after_seconds:
        set_periodically()

    if get_faiss_resources:
        get_faiss_resources()

    set_faiss_index()
