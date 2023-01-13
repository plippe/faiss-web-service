from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from faiss_index.faiss_index import FaissIndex

blueprint = Blueprint('faiss_index', __name__)

@blueprint.record_once
def record(setup_state):
    blueprint.faiss_index = FaissIndex(
        setup_state.app.config.get('INDEX_PATH'),
        setup_state.app.config.get('IDS_VECTORS_PATH'))

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
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500
