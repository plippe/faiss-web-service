import numpy as np
import logging
import faiss
import pickle
import sys

sys.path.append("..")
from utils.feature_detect import *
from config import *


# prepare index
dimensions = SIFT_DIMENSIONS
if isAddPhash:
    dimensions += PHASH_X * PHASH_Y

index = faiss.index_factory(dimensions, INDEX_KEY)
# index = faiss.IndexIDMap(index)
if USE_GPU:
    print("Use GPU...")
    res = faiss.StandardGpuResources()
    index = faiss.index_cpu_to_gpu(res, 0, index)

# start training
images_list = iterate_files(train_image_dir)
# prepare ids
ids_count = 0
index_dict = {}
ids = None
features = np.matrix([])
sift = get_sift()
for file_name in images_list:
    ret, sift_feature = calc_sift(sift, file_name)
    if ret == 0 and sift_feature.any():
        # record id and path
        image_dict = {ids_count: (file_name, sift_feature)}
        index_dict.update(image_dict)
        # print ids_count
        # print sift_feature.shape[0]
        ids_list = np.linspace(ids_count, ids_count, num=sift_feature.shape[0], dtype="int64")
        ids_count += 1
        if features.any():
            features = np.vstack((features, sift_feature))
            ids = np.hstack((ids, ids_list))
        else:
            features = sift_feature
            ids = ids_list
        if ids_count % 500 == 499:
            if not index.is_trained and INDEX_KEY != "IDMap,Flat":
                index.train(features)
            index.add_with_ids(features, ids)
            ids = None
            features = np.matrix([])

if features.any():
    if not index.is_trained and INDEX_KEY != "IDMap,Flat":
        index.train(features)
    index.add_with_ids(features, ids)

# save index
faiss.write_index(index, index_path)

# save ids
with open(ids_vectors_path, 'wb+') as f:
    try:
        pickle.dump(index_dict, f, True)
    except EnvironmentError as e:
        logging.error('Failed to save index file error:[{}]'.format(e))
        f.close()
    except RuntimeError, v:
        logging.error('Failed to save index file error:[{}]'.format(v))
f.close()
