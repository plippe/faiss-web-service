import numpy as np
import faiss
import sys
import time

sys.path.append("..")
from config import *

start_time = time.time()
print(start_time)

if len(sys.argv) < 5:
    print("train_ids_path train_features_path add_ids_path add_features_path index_output_path")
    sys.exit()

train_ids_path = sys.argv[1]
train_features_path = sys.argv[2]
add_ids_path = sys.argv[3]
add_features_path = sys.argv[4]
index_output_path = sys.argv[5]

# prepare index1
dimensions = SIFT_DIMENSIONS
index = faiss.index_factory(dimensions, INDEX_KEY)
# index1 = faiss.IndexIDMap(index1)
if USE_GPU:
    print("Use GPU...")
    res = faiss.StandardGpuResources()
    index = faiss.index_cpu_to_gpu(res, 0, index)

print("start read train ids")
ids_array = np.fromfile(train_ids_path, sep=' ', dtype='int64')
print("start read train features")
features_array = np.fromfile(train_features_path, sep=' ', dtype='>f4')
print("start reshape")
features_count = len(ids_array)
features = features_array.reshape((features_count, dimensions))
print("start train index1")
index.train(features)
index.add_with_ids(features, ids_array)
print("train index1 done. features count: " + str(features_count))

print("start read add ids")
ids_array = np.fromfile(add_ids_path, sep=' ', dtype='int64')
print("start read add features")
features_array = np.fromfile(add_features_path, sep=' ', dtype='>f4')
print("start reshape")
features_count = len(ids_array)
features = features_array.reshape((features_count, dimensions))
print("start add ids & features in index1")
index.add_with_ids(features, ids_array)
print("add done. features count: " + str(features_count))

# save index1
if USE_GPU:
    index = faiss.index_gpu_to_cpu(index)
faiss.write_index(index, index_output_path)
print("save index1 to file done: " + index_output_path)

process_time = time.time() - start_time
print(process_time)

