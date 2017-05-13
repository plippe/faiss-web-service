import os
import faiss
import pickle
import numpy as np

indexes_path = os.path.dirname(os.path.realpath(__file__))
index_file = os.path.join(indexes_path, 'index')
ids_vectors_file = os.path.join(indexes_path, 'ids_vectors.p')

np.random.seed(1234)

d = 64
nb = 100000
nq = 10000
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.

ids = (np.random.random(xb.shape[0]) * nb).astype('int')

index = faiss.IndexFlatL2(xb.shape[1])
index_with_ids = faiss.IndexIDMap(index)
index_with_ids.add_with_ids(xb, ids)

faiss.write_index(index_with_ids, index_file)

id_vector = dict(zip(ids, xb))
with open(ids_vectors_file, 'wb') as outfile:
    pickle.dump(id_vector, outfile)
