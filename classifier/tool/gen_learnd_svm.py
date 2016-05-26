import pickle
import numpy as np
import os
from classifier.svm import sift_bof, im


def generate(svm_name = 'unnamed', pathes = ['./']):
    encode_path = 'learned/'

    extensions = ['jpg', 'png']
    dvector_len = 1000

    images = []
    classes = []
    for ipath in range(len(pathes)):
        classimages = im.imsread_ext(dirpath=pathes[ipath], flags=0, exts=extensions)
        images.extend(classimages)
        classes.extend(((np.ones(len(classimages), dtype=np.int))*ipath).tolist())

    img_and_cls = list(zip(images, classes))

    with open(encode_path+svm_name + '.pkl', "wb") as f:
        pickle.dump(sift_bof.create(img_and_cls, dvector_len), f)


pathes = [
    '../datasets/Gtra/', # class 0
    '../datasets/Gneg/'] # class 1
generate(svm_name='g', pathes=pathes)