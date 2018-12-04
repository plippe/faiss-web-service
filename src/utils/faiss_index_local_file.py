def GET_FAISS_INDEX():
    import faiss
    from config import index_path

    index = faiss.read_index(index_path)
    return index


def GET_FAISS_ID_TO_VECTOR():
    import pickle
    from config import ids_vectors_path
    import os

    if not os.path.exists(ids_vectors_path):
        return None

    with open(ids_vectors_path, 'rb') as f:
        index_dict = pickle.load(f)

    def id_to_vector(id_):
        try:
            return index_dict[id_]
        except:
            pass

    return id_to_vector

