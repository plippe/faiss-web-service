DEBUG = True


def GET_FAISS_RESOURCES():
    return None


def GET_FAISS_INDEX():
    raise NotImplementedError


def GET_FAISS_ID_TO_VECTOR():
    raise NotImplementedError


UPDATE_FAISS_AFTER_SECONDS = None

IMAGESEARCH_TMP = "/tmp/search/"

# --------------------- Feature Detect
# resize size
NOR_X = 512
NOR_Y = 384

# phash size
PHASH_X = 8
PHASH_Y = 8

SIFT_DIMENSIONS = 128

# feature's count extracted from each image
NUM_FEATURES = 100
isAddPhash = False

# BoW
bow_num_words = 1000
dictionary_path = '/faiss-web-service/resources/dictionary'
# NUM_FEATURES = 0
# isAddPhash = False

# --------------------- Train
# INDEX_KEY = "IDMap,Flat"
INDEX_KEY = "IDMap,IMI2x10,Flat"
# INDEX_KEY = "IDMap,OPQ16_64,IMI2x12,PQ8+16"
USE_GPU = True

train_image_dir = "/images/0001e8b70ae2307593a59be324f3ad15"
index_path = "/faiss-web-service/resources/index"
ids_vectors_path = '/faiss-web-service/resources/ids_paths_vectors'

# ---------------------  Search
TOP_N = 5
SIMILARITY = 5
