import os
import faiss
import pickle

class Configuration(object):
    DEBUG = True

    @staticmethod
    def get_indexes_file(filename):
        indexes_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(indexes_path, '..', 'indexes', filename)

    @staticmethod
    def FAISS_INDEX():
        index_file_path = Configuration.get_indexes_file('index')
        return faiss.read_index(index_file_path)

    @staticmethod
    def FAISS_IDS_VECTORS():
        ids_vectors_path = Configuration.get_indexes_file('ids_vectors.p')
        with open(ids_vectors_path, 'rb') as f:
            return pickle.load(f)
