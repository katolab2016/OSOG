from classifier.svm.sift_bof import SVM

import cv2

img = cv2.imread("../../datasets/Gtra/G_001.JPG", 0)

svm = SVM(svm_name='g')

result = svm.predict(img)

print(result)