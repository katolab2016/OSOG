import math
import random

import cv2
import numpy as np
from sklearn.metrics import accuracy_score

from classifier.svm import sift_bof as ss
from classifier.tool import file


dvector_len = 1000
sift = cv2.xfeatures2d.SIFT_create()

#データセット読み込み
exts = ['jpg', 'png']
dirs = [
    '../../datasets/G/',
    '../../datasets/beetle/',
    '../../datasets/cricket/',
    '../../datasets/stagbeetle/'
]
div_ratio = 0.9
icz = file.read_dataset(dirs, exts=exts, size=(96,96))
random.shuffle(icz)
train = icz[:math.floor(div_ratio * len(icz))]
test = icz[math.floor(div_ratio * len(icz)):]

svm, visual_words = ss.create(train, dvector_len)

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
