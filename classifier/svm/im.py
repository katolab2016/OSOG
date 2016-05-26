import cv2
import os
import fnmatch

# read images with the extension match from directory
def imsread_ext(dirpath='./', flags=1, exts=None):
    filelist = os.listdir(dirpath)

    namelist = []
    imglist = []

    if exts is None:
        namelist = filelist
    else:
        for ext in exts:
            namelist.extend(fnmatch.filter(filelist, '*.' + ext))

    for name in namelist:
        imglist.append(cv2.imread(dirpath + name, flags))

    return imglist