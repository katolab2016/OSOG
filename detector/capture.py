from idlelib.run import handle_tk_events
import numpy as np
import cv2
import random
import os
import sys
from osog.classifier.universal import Estimator
from osog.detector.color_filter import hsv
from matplotlib import pyplot as plt

DEBUG = False

def flame_sub(im1, im2, im3, th, blur):

    d1 = cv2.absdiff(im3, im2)
    d2 = cv2.absdiff(im2, im1)
    diff = cv2.bitwise_and(d1, d2)

    #差分が閾値より小さければTrue
    mask = diff < th

    #背景画像と同じサイズの配列生成
    im_mask = np.empty((im1.shape[0], im1.shape[1]), np.uint8)
    im_mask[:][:] = 255

    #true部分(背景)は黒塗り
    im_mask[mask] = 0

    #ゴマ塩ノイズ除去
    im_mask = cv2.medianBlur(im_mask,blur)

    return im_mask

class GDetector:

    def __init__(self):
        self.cam = cv2.VideoCapture(1)
        self.im1 = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_BGR2GRAY)
        self.im2 = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.estimator = Estimator(estimator_type='DNN', model_name='6class2')
        self.predict = np.zeros(1).tolist()
        self.number=0

    #Gがいるか?
    def exists(self, camera_enable):
        #フレーム間差分計算
        im4 = self.cam.read()[1]
        self.im3 = cv2.cvtColor(im4, cv2.COLOR_RGB2GRAY)
        im_fs = flame_sub(self.im1, self.im2, self.im3, 5, 7)

        brown = hsv(im4)
        area = cv2.bitwise_and(im_fs, brown)
        ret, thresh = cv2.threshold(area, 127, 255, 0)

        cnt,im , _ = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
        x,y,w,h = cv2.boundingRect(cnt)
        new_w = h if h > w else w
        new_h = w if w > h else h
        # new_x = x - (int(new_w / 2 - w / 2))
        new_x = x - (new_w - w) // 2 if x > (new_w - w) // 2 else x
        new_y = y - (new_h - h) // 2 if y > (new_h - h) // 2 else y
        # cv2.rectangle(im4, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.rectangle(im4, (new_x, new_y), (new_x + new_w, new_y + new_h), (0, 255, 0), 2)
        dst = im4[new_y:new_y + new_h, new_x:new_x + new_w]
        #cv2.imwrite('dst.jpg', dst)

        #識別機にわたすとこやでー
        #仮の処理
        if len(dst) > 0:
            predicted_class, predicted_prob = self.estimator.predict(dst)
        else:
            predicted_class = 6
        #識別機からもらうでー

        self.im1 = self.im2
        self.im2 = self.im3

        if False and predicted_class < 6 and predicted_prob >= 0:
            if predicted_class == 0:
                print('G(toy)\t%s%%' %predicted_prob)
            elif predicted_class == 1:
                print('G(real)\t%s%%' %predicted_prob)
            elif predicted_class == 2:
                print('カブトムシ\t%s%%' %predicted_prob)
            elif predicted_class == 3:
                print('コオロギ\t%s%%' %predicted_prob)
            elif predicted_class == 4:
                print('クワガタ\t%s%%' %predicted_prob)
            elif predicted_class == 5:
                print('手\t\t%s%%'%predicted_prob)

        if predicted_class == 0 or predicted_class == 1:
            self.number+=1
        else:
            self.number=0
        if self.number >= 6:
            exist = True
            sys.stdout.flush()
            sys.stdout.write('\rGがいる')
        else:
            exist = False
            sys.stdout.flush()
            sys.stdout.write('\rGはいない')

        if camera_enable:
            cv2.imshow('Input', im4)
        else:
            cv2.destroyWindow('Input')
        if DEBUG:
            cv2.imshow("Motion Mask", area)

        return dst, exist


