from osog.classifier.svm.sift_bof import SVM
from osog.classifier.dnn.cnn import CNN
import cv2

class Estimator:
    def __init__(self, estimator_type=None, model_name=None):
        self.estimator_type = estimator_type

        if self.estimator_type == 'SVM':
            self.estimator = SVM(svm_name=model_name)

        elif self.estimator_type == 'DNN':
            self.estimator = CNN(dnn_name=model_name)

        else:
            print('Error: unexpected estimator type %s' %estimator_type)

    def predict(self, image):
        image = cv2.resize(image, (32,32))

        if self.estimator_type == 'SVM':
            return self.estimator.predict(image),1
        elif self.estimator_type == 'DNN':
            return self.estimator.predict(image)

