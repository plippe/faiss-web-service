def GET_FAISS_RESOURCES():
    import os
    import urllib

    tmp_folder = '/tmp/faiss-web-service'
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    github_repo = 'https://github.com/Plippe/faiss-web-service/raw/70e2b1c176e420ca10838e3681fe12f97e80142f'
    urllib.urlretrieve(github_repo + '/faiss_index_files/index', filename=tmp_folder + '/index')
    urllib.urlretrieve(github_repo + '/faiss_index_files/ids_vectors.p', filename=tmp_folder + '/ids_vectors.p')

def GET_FAISS_INDEX():
    import faiss

    index_file_path = '/tmp/faiss-web-service/index'
    return faiss.read_index(index_file_path)

def GET_FAISS_ID_TO_VECTOR():
    import pickle

    ids_vectors_path = '/tmp/faiss-web-service/ids_vectors.p'
    with open(ids_vectors_path, 'rb') as f:
        ids_vectors = pickle.load(f)

    def id_to_vector(id_):
        try:
            return ids_vectors[id_]
        except:
            pass

    return id_to_vector


UPDATE_FAISS_AFTER_SECONDS = 60 * 60 # every hour

