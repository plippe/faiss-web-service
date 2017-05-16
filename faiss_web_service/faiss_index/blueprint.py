from flask import Blueprint, jsonify, request
from faiss_index import FaissIndex

blueprint = Blueprint('faiss_index', __name__)

@blueprint.record
def record(setup_state):
    manage_faiss_index(
        setup_state.app.config.get('GET_FAISS_RESOURCES'),
        setup_state.app.config['GET_FAISS_INDEX'],
        setup_state.app.config['GET_FAISS_IDS_VECTORS'],
        setup_state.app.config.get('UPDATE_FAISS_AFTER_SECONDS'))

@blueprint.route('/faiss')
def search():
    ids = request.args.getlist('ids', type=int)
    k = request.args.get('k', type=int)

    try:
        results = blueprint.faiss_index.search_by_ids(ids, k)
        return jsonify(results)
    except:
        return jsonify([])

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
