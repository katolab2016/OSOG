import fnmatch
import os
import math
import cv2
import numpy as np
import matplotlib as mpl
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.cluster import MiniBatchKMeans
import time

def create(img_and_cls, dvector_len):
    start = time.time()
    images, classes = map(list, zip(*img_and_cls))
    local_features = []
    global_features = []
    sift = cv2.xfeatures2d.SIFT_create()
    clf = SVC(kernel='rbf', C=10000)

    # すべての画像の特徴量を取り出す
    for img in images:
        local_features.append(sift.detectAndCompute(img, None)[1])
    eft = np.concatenate(list(filter(lambda f: f is not None, local_features)))
    visual_words = MiniBatchKMeans(n_clusters=dvector_len).fit(eft).cluster_centers_

    for i in range(len(images)):
        dvector = np.zeros(dvector_len)
        if local_features[i] is not None:
            for f in local_features[i]:
                dvector[((visual_words - f) ** 2).sum(axis=1).argmin()] += 1
            dvector = dvector/sum(dvector)
        global_features.append(dvector)

    clf.fit(global_features, classes)

    return clf, visual_words


# read images with the extension match from directory
def imsread_ext(dirpath='./', flags=1, exts=None):
    filelist = os.listdir(dirpath)

    namelist = []
    imglist = []

    if exts is None:
        namelist = filelist
    else:
        for ext in exts:
            namelist.extend(fnmatch.filter(filelist, '*.' + ext))

    for name in namelist:
        imglist.append(cv2.imread(dirpath + name, flags))

    return imglist
