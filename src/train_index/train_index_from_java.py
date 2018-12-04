import numpy as np
import faiss
import sys
import time

sys.path.append("..")
from utils.feature_detect import *
from utils.read_array_from_java import reshape_array
from config import *

# prepare index
dimensions = SIFT_DIMENSIONS
index = faiss.index_factory(dimensions, INDEX_KEY)
# index = faiss.IndexIDMap(index)
if USE_GPU:
    print("Use GPU...")
    res = faiss.StandardGpuResources()
    index = faiss.index_cpu_to_gpu(res, 0, index)

# start training
# file_path = "/tmp/test/test.txt"

file_path = sys.argv[1]

ids = []
features_array_str = ""

start_time = time.time()
print(start_time)
print("start train index from java output file....")
line_count = 0
with open(file_path, 'r') as f:
    for line in f:
        line_count += 1
        arr = line.split(":")
        id = int(arr[0])
        feature_count = len(arr[1].split(" ")) / dimensions
        ids_list = np.linspace(id, id, num=feature_count, dtype="int64")
        print("append ids")
        ids = np.append(ids, ids_list)
        print("append features_array_str")
        if features_array_str == "":
            features_array_str = arr[1]
        else:
            features_array_str = features_array_str + " " + arr[1]
        if line_count % 100 == 0:
            print line_count
        if INDEX_KEY == "IDMap,IMI2x10,Flat" and not index.is_trained and len(ids) >= 1048576:
            print("start reshape train features: " + str(len(ids)))
            f_array = np.array(features_array_str.split(" "), dtype=">f4")
            features = reshape_array(f_array, dimensions)
            print("start train index")
            index.train(features)
            index.add_with_ids(features, ids)
            ids = []
            features_array = []
        elif index.is_trained:
            f_array = np.array(features_array_str.split(" "), dtype=">f4")
            features = reshape_array(f_array, dimensions)
            index.add_with_ids(features, ids)
            ids = []
            features_array_str = ""

if len(ids) > 0:
    f_array = np.array(features_array_str.split(" "), dtype=">f4")
    features = reshape_array(f_array, dimensions)
    if not index.is_trained and INDEX_KEY != "IDMap,Flat":
        index.train(features)
    index.add_with_ids(features, ids)
    # print features
    # print ids

print("train index done ....")
print("Images count: " + str(line_count))
# save index
faiss.write_index(index, index_path)
print("save index to file done: " + index_path)

process_time = time.time() - start_time
print(process_time)