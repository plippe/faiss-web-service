import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

class FaissIndex(object):

    # def __init__(self, index_path, ids_vectors_path):
    #     assert(index_path)
    #     assert(ids_vectors_path)

    #     import pickle
    #     with open(ids_vectors_path, 'rb') as f:
    #         ids_vectors = pickle.load(f, encoding='latin1')

    #     def id_to_vector(id_):
    #         try:
    #             return ids_vectors[id_]
    #         except:
    #             pass

    #     self.index = faiss.read_index(index_path)
    #     self.id_to_vector = id_to_vector

    def __init__(self, json_path):
        # self.index = faiss.read_index(json_path) ##
        # self.id_to_vector = id_to_vector
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        
        df = pd.read_json(json_path)
        df['searchColumn'] = df['title'] + " " + df['description']
        sentences = df['searchColumn'].tolist()

        sentence_embeddings = self.get_embeddings(sentences)

        d = sentence_embeddings.shape[1] # 768
        nlist = 100
        bits = 8 # number of bits in each centroid
        m = 8 # number of centroid IDs in final compressed vectors
        quantizer = faiss.IndexFlatL2(d)  # this remains the same
        self.index = faiss.IndexIVFPQ(quantizer, d, nlist, m, bits)
                                        # 8 specifies that each sub-vector is encoded as 8 bits
        self.index.train(sentence_embeddings)
        self.index.add(sentence_embeddings)

        D, I = self.search_by_sentence("war in ukrain") # sanity check
        print(I)
        print(D)

    def get_embedding(self, sentence):
        sentence_embedding = self.model.encode(sentence)
        return sentence_embedding

    def get_embeddings(self, sentences):
        sentence_embeddings = self.model.encode(sentences)
        return sentence_embeddings


    def search_by_sentence(self, sentence, k = 4):
        return self.index.search(sentence, k)

    def search_by_ids(self, ids, k):
        vectors = [self.id_to_vector(id_) for id_ in ids]
        results = self.__search__(ids, vectors, k + 1)

        return results

    def search_by_vectors(self, vectors, k):
        ids = [None] * len(vectors)
        results = self.__search__(ids, vectors, k)

        return results

    def __search__(self, ids, vectors, k):
        def neighbor_dict(id_, score):
            return { 'id': int(id_), 'score': float(score) }

        def result_dict(id_, vector, neighbors):
            return { 'id': id_, 'vector': vector.tolist(), 'neighbors': neighbors }

        results = []

        vectors = [np.array(vector, dtype=np.float32) for vector in vectors]
        vectors = np.atleast_2d(vectors)

        scores, neighbors = self.index.search(vectors, k) if vectors.size > 0 else ([], [])
        for id_, vector, neighbors, scores in zip(ids, vectors, neighbors, scores):
            neighbors_scores = zip(neighbors, scores)
            neighbors_scores = [(n, s) for n, s in neighbors_scores if n != id_ and n != -1]
            neighbors_scores = [neighbor_dict(n, s) for n, s in neighbors_scores]

            results.append(result_dict(id_, vector, neighbors_scores))

        return results
