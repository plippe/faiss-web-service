from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from sqlalchemy import true
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
        tupleList = list(zip(I[0], D[0]))
        res = sorted(
            [{"index": int(i), "match": float(d)} for i, d in tupleList if i != -1],
            key=lambda x: x["match"]
        )
        return jsonify({'res': res})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500


@blueprint.route('/faiss/add', methods=['POST'])
def add():
    try:
        json = request.get_json(force=True)
        id = json['id']
        sentence = json['sentence']
        res = blueprint.faiss_index.add_with_id(id, sentence)
        return jsonify({'res': "success"})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500


@blueprint.route('/faiss/remove', methods=['DELETE'])
def remove():
    try:
        json = request.get_json(force=True)
        id = json['id']
        res = blueprint.faiss_index.remove_by_id(id)
        return jsonify({'res': "success"})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500
