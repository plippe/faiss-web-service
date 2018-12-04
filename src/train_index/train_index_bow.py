import numpy as np
import logging
import faiss
import pickle
import sys

sys.path.append("..")
from utils.feature_detect import *
from config import *

images_list = iterate_files(train_image_dir)
print len(images_list)

# ------------------- get dictionary
sift = cv2.xfeatures2d.SIFT_create(nfeatures=NUM_FEATURES)
if not os.path.exists(dictionary_path):
    # get features
    BOW = cv2.BOWKMeansTrainer(bow_num_words)
    for file_name in images_list:
        ret, sift_feature = calc_sift(sift, file_name)
        if ret == 0 and sift_feature.any():
            BOW.add(sift_feature)

    # get words
    dictionary = BOW.cluster()

    # save dictionary
    with open(dictionary_path, 'wb+') as f:
        pickle.dump(index_dict, f, True)
    f.close()
else:
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f)

bowDiction = cv2.BOWImgDescriptorExtractor(sift, cv2.BFMatcher(cv2.NORM_L2))
bowDiction.setVocabulary(dictionary)
print "bow dictionary", np.shape(dictionary)


# returns descriptor of image at pth
def feature_extract(pth):
    im = cv2.imread(pth, 1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return bowDiction.compute(gray, sift.detect(gray))


# ------------------- train faiss index
# prepare index
index = faiss.index_factory(bow_num_words, INDEX_KEY)
# index = faiss.IndexIDMap(index)
if USE_GPU:
    print("Use GPU...")
    res = faiss.StandardGpuResources()
    index = faiss.index_cpu_to_gpu(res, 0, index)

# prepare ids
ids_count = 1
index_dict = {}
ids = []
features = np.matrix([])

for file_name in images_list:
    print ids_count
    dsc = feature_extract(file_name)
    # record id and path
    image_dict = {ids_count: (file_name, dsc)}
    index_dict.update(image_dict)
    ids.append(ids_count)
    ids_count += 1
    if features.any():
        features = np.vstack((features, dsc))
    else:
        features = dsc

    if ids_count % 500 == 1:
        print ids_count
        if not index.is_trained and INDEX_KEY != "IDMap,Flat":
            index.train(features)
        index.add_with_ids(features, np.array(ids))
        ids = []
        features = np.matrix([])

print features.shape
print len(ids)

if features.any():
    if not index.is_trained and INDEX_KEY != "IDMap,Flat":
        index.train(features)
    index.add_with_ids(features, np.array(ids))

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
