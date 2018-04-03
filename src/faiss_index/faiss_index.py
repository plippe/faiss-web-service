import faiss
import numpy as np

class FaissIndex(object):

    def __init__(self, index, id_to_vector):
        assert index
        assert id_to_vector

        self.index = index
        self.id_to_vector = id_to_vector

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
            return { 'id': long(id_), 'score': float(score) }

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
