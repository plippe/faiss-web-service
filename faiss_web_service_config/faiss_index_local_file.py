def FAISS_INDEX():
    import faiss

    index_file_path = '/opt/faiss-web-service/faiss_index_files/index'
    return faiss.read_index(index_file_path)

def FAISS_IDS_VECTORS():
    import pickle

    ids_vectors_path = '/opt/faiss-web-service/faiss_index_files/ids_vectors.p'
    with open(ids_vectors_path, 'rb') as f:
        return pickle.load(f)
