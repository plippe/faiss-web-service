from flask import Blueprint, jsonify, request
from faiss_index import FaissIndex

blueprint = Blueprint('faiss_index', __name__)

@blueprint.record
def record(setup_state):
    index = setup_state.app.config['FAISS_INDEX']()
    ids_vectors = setup_state.app.config['FAISS_IDS_VECTORS']()

    blueprint.faiss_index = FaissIndex(index, ids_vectors)

@blueprint.route('/faiss')
def search():
    ids = request.args.getlist('ids', type=int)
    k = request.args.get('k', type=int)

    try:
        results = blueprint.faiss_index.search_by_ids(ids, k)
        return jsonify(results)
    except:
        return jsonify([])
