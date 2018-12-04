import numpy as np
import os
import cv2
import logging
import uuid
import sys

sys.path.append("..")
from config import *


# ------------- Get PHash
def calc_phash(gray_image):
    img = gray_image
    img = cv2.resize(img, (PHASH_X, PHASH_Y), interpolation=cv2.INTER_CUBIC)
    # create 2D array
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img
    # convert 2D array
    vis1 = cv2.dct(cv2.dct(vis0))
    vis1.resize(PHASH_X, PHASH_Y)
    # convert to flat
    img_list = vis1.flatten()
    # mean value
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = [np.float32(0) if i < avg else np.float32(1) for i in img_list]
    return np.matrix(avg_list).flatten()


# ------------- add Phash featrue
def adddPhash(gray_image, des):
    phash = calc_phash(gray_image)
    # merge phash and sift
    n, d = des.shape
    phash_mat = phash
    for i in range(n - 1):
        phash_mat = np.vstack((phash_mat, phash))
    des = np.hstack((des, phash_mat))
    return des


# ------------- Get SIFT Feature
def calc_sift(sift, image_file):
    if not os.path.isfile(image_file):
        logging.error('Image:{} does not exist'.format(image_file))
        return -1, None

    try:
        image_o = cv2.imread(image_file)
    except:
        logging.error('Open Image:{} failed'.format(image_file))
        return -1, None

    if image_o is None:
        logging.error('Open Image:{} failed'.format(image_file))
        return -1, None

    image = cv2.resize(image_o, (NOR_X, NOR_Y))
    if image.ndim == 2:
        gray_image = image
    else:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kp, des = sift.detectAndCompute(gray_image, None)

    if isAddPhash:
        des = adddPhash(gray_image, des)

    sift_feature = np.matrix(des)
    return 0, sift_feature


def iterate_files(_dir):
    result = []
    for root, dirs, files in os.walk(_dir, topdown=True):
        for fl in files:
            if fl.endswith("jpg") or fl.endswith("JPG"):
                result.append(os.path.join(root, fl))
    return result


def save_tmp_image(base64_str):
    img_data = base64_str.decode('base64')
    file_postfix = str(uuid.uuid1()) + ".jpg"
    filename = os.path.join(IMAGESEARCH_TMP, file_postfix)
    fw = open(filename, 'wb')
    fw.write(img_data)
    fw.close()
    return filename


def get_vectors(sift, image):
    # if is base64 string
    # image = save_tmp_image(image)
    # if is image path
    return calc_sift(sift, image)


def get_sift():
    return cv2.xfeatures2d.SIFT_create(nfeatures=NUM_FEATURES, nOctaveLayers=3, contrastThreshold=0.04,
                                       edgeThreshold=10, sigma=1.6)
