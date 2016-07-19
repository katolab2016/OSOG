import cv2
import os
import fnmatch
import numpy as np

# read images with the extension match from directory
def imsread_ext(dirpath='./', flags=1, size=(28,28), exts=None):
    filelist = os.listdir(dirpath)

    namelist = []
    imglist = []

    if exts is None:
        namelist = filelist
    else:
        for ext in exts:
            namelist.extend(fnmatch.filter(filelist, '*.' + ext))

    for name in namelist:
        image =cv2.imread(dirpath + name, flags)
        if flags == 1 and image is None:
          print('%s is invalid format' % name )
        elif len(image) == len(image[0]):
            imglist.append(cv2.resize(image, size))
        else:
            print('サイズ不適合により無視: %s' % name)

    return imglist

# read images with class label
def read_dataset(dirpathes, flags=1, size=(28,28), exts=None):

    images = []
    classes = []
    for ipath in range(len(dirpathes)):
        classimages = imsread_ext(dirpath=dirpathes[ipath], flags=flags, size=size, exts=exts)
        images.extend(classimages)
        classes.extend(((np.ones(len(classimages),dtype=np.int)) * ipath).tolist())

    return list(zip(images, classes))

