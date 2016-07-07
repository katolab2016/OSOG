from osog.classifier.dnn.cnn import CNN
from osog.classifier.tool.file import *

#識別器のインスタンス生成
estimator = CNN(dnn_name='../learned/model6')
images = imsread_ext(dirpath='../../datasets/beetle/', flags=1, size=(32,32),exts=['jpg','png'])

for i in images:
    print(estimator.predict(i))
