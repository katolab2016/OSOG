from osog.classifier.svm.sift_bof import SVM
# from osog.classifier.dnn

class Estimator:
    def __init__(self, estimator_type=None, model_name=None):

        if estimator_type == 'SVM':
            self.estimator = SVM(svm_name=model_name)

        elif estimator_type == 'DNN':
            print('skelton')

        else:
            print('unexpected estimator type %s' %estimator_type)


