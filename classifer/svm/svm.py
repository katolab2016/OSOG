import math
import random

import cv2
import numpy as np
from sklearn.metrics import accuracy_score

from classifer.svm import sift_svm as ss

path_pos = './datasets/Gtra/'
path_neg = './datasets/Gneg/'
div_ratio = 0.5
dvector_len = 1000
extensions = ['jpg', 'png']
sift = cv2.xfeatures2d.SIFT_create()

images_pos = ss.imsread_ext(dirpath=path_pos, flags=0, exts=extensions)
print("positive class image num is "+str(len(images_pos)))
images_neg = ss.imsread_ext(dirpath=path_neg, flags=0, exts=extensions)
print("negative class image num is "+str(len(images_neg)))

images = images_pos + images_neg
classes = np.zeros(len(images_pos),dtype=np.int).tolist() + np.ones(len(images_neg),dtype=np.int).tolist()

img_and_cls = list(zip(images, classes))
random.shuffle(img_and_cls)

train = img_and_cls[:math.floor(div_ratio*len(images))]
test = img_and_cls[math.floor(div_ratio*len(images)):]
print("Load image has been Completed.")
svm , visual_words = ss.create(train, dvector_len)
print("Initialize has been Completed.")

test_images, test_classes = map(list, zip(*test))

test_features = []
for img in test_images:
    feat = sift.detectAndCompute(img, None)[1]
    dvector = np.zeros(dvector_len)
    if feat is not None:
        for f in feat:
            dvector[((visual_words - f) ** 2).sum(axis=1).argmin()] += 1
        dvector = dvector / sum(dvector)
    test_features.append(dvector)
forecast_classes = svm.predict(test_features)
score = accuracy_score(forecast_classes, test_classes)
print(score)