import heapq
import numpy as np
import sys

sys.path.append("..")
from utils.feature_detect import get_vectors, get_sift
from config import NUM_FEATURES, SIFT_DIMENSIONS, SIMILARITY
from utils.read_array_from_java import read_array


class FaissIndex(object):

    def __init__(self, index, id_to_vector):
        assert index
        # assert id_to_vector

        self.index = index
        self.id_to_vector = id_to_vector
        self.sift = get_sift()

    def search_by_ids(self, ids, k):
        vectors = [self.id_to_vector(id_)[1] for id_ in ids]
        results = self.__search__(ids, vectors, k + 1)

        return results

    def search_by_vectors(self, vectors, k):
        vectors = read_array(vectors, SIFT_DIMENSIONS)
        # ====== trick code start ===========
        count = vectors.shape[0]
        vectors = np.vstack((vectors, vectors))
        vectors = vectors[0:count, :]
        print vectors.shape
        # ====== trick code end ===========
        ids = [None]
        results = self.__search__(ids, [vectors], k)
        return results

    def search_by_image(self, image, k):
        ids = [None]
        ret, vectors = get_vectors(self.sift, image)
        results = self.__search__(ids, [vectors], k)

        return results

    def __search__(self, ids, vectors, topN):
        def neighbor_dict_with_path(id_, file_path, score):
            return {'id': long(id_), 'file_path': file_path, 'score': score}

        def neighbor_dict(id_, score):
            return {'id': long(id_), 'score': score}

        def result_dict_str(id_, neighbors):
            return {'id': id_, 'neighbors': neighbors}

        results = []
        need_hit = SIMILARITY

        for id_, siftfeature in zip(ids, vectors):
            scores, neighbors = self.index.search(siftfeature, k=topN) if siftfeature.size > 0 else ([], [])
            n, d = neighbors.shape
            result_dict = {}

            for i in range(n):
                l = np.unique(neighbors[i]).tolist()
                for r_id in l:
                    if r_id != -1:
                        score = result_dict.get(r_id, 0)
                        score += 1
                        result_dict[r_id] = score

            h = []
            for k in result_dict:
                v = result_dict[k]
                if v >= need_hit:
                    if len(h) < topN:
                        heapq.heappush(h, (v, k))
                    else:
                        heapq.heappushpop(h, (v, k))

            result_list = heapq.nlargest(topN, h, key=lambda x: x[0])
            neighbors_scores = []
            for e in result_list:
                confidence = e[0] * 100 / n
                if self.id_to_vector:
                    file_path = self.id_to_vector(e[1])[0]
                    neighbors_scores.append(neighbor_dict_with_path(e[1], file_path, str(confidence)))
                else:
                    neighbors_scores.append(neighbor_dict(e[1], str(confidence)))
            results.append(result_dict_str(id_, neighbors_scores))
        return results
