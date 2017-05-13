import faiss
import numpy as np

class FaissIndex(object):

    def __init__(self, index, ids_vectors):
        assert index
        assert ids_vectors

        self.index = index
        self.ids_vectors = ids_vectors

    def search_by_id(self, id_, k):
        results = self.search_by_ids([id_], k)
        return results[0] if results else None

    def search_by_ids(self, ids, k):
        ids = [id_ for id_ in ids if id_ in self.ids_vectors]
        vectors = [self.ids_vectors[id_] for id_ in ids]
        results = self.__search__(ids, vectors, k)

        return results

    def __search__(self, ids, vectors, k):
        def neighbor_dict(id_, score):
            return { 'id': long(id_), 'score': float(score) }

        def result_dict(id_, neighbors):
            return { 'id': id_, 'neighbors': neighbors }

        results = []

        vectors = [np.array(vector, dtype=np.float32) for vector in vectors]
        vectors = np.atleast_2d(vectors)

        scores, neighbors = self.index.search(vectors, k + 1)
        for id_, neighbors, scores in zip(ids, neighbors, scores):
            neighbors_scores = [neighbor_dict(n, s) for n, s in zip(neighbors, scores)]
            neighbors_scores_without_self = [ns for ns in neighbors_scores if ns['id'] != id_]
            results.append(result_dict(id_, neighbors_scores_without_self))

        return results
