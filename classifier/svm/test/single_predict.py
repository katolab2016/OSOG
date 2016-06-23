from classifier.svm.sift_bof import SVM
import cv2
import os

#判定する画像の読み込み
img = cv2.imread('../../datasets/G/G2.jpg' , 0)

#SVM(svm_name='使用するSVMの名前(拡張子なしで)')
svm = SVM(svm_name='0623')

#読み込んだオブジェクトのpredictメソッドに判定したい画像を渡す
result = svm.predict(img)

#結果の出力
print(result)