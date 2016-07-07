import pickle
import numpy as np
import os
from osog.classifier.svm import sift_bof
from osog.classifier.tool import file


def generate(svm_name = 'unnamed', dirs = ['./']):
    # conficuration
    encode_path = ''
    extensions = ['jpg', 'png']
    dvector_len = 1000

    print('Loading datasets ...')
    icz = file.read_dataset(dirs, exts=extensions, size=(32, 32))
    print('Datasets Loaded.')

    print('Learning and Saving ...')
    with open(encode_path+svm_name + '.pkl', "wb") as f:
        pickle.dump(sift_bof.create(icz, dvector_len), f)
    print('SVM created.')

if __name__ == '__main__':
    pathes = [
        '../datasets/G/', # class 0
        '../datasets/beetle/', # class 1
        '../datasets/cricket/', # class 2
        '../datasets/stagbeetle/' ]# class 3

    generate(svm_name='0623', dirs=pathes)