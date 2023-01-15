from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from faiss_index.faiss_index import FaissIndex

blueprint = Blueprint('faiss_index', __name__)


@blueprint.record_once
def record(setup_state):
    blueprint.faiss_index = FaissIndex(
        setup_state.app.config.get('PINS_JSON_PATH')
        # setup_state.app.config.get('INDEX_PATH'),
        # setup_state.app.config.get('IDS_VECTORS_PATH')
    )


@blueprint.route('/faiss/search')
def search():
    try:
        q = request.args.get('q')
        D, I = blueprint.faiss_index.search_by_sentence(q)
        return jsonify({'d': D, 'i': I})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500