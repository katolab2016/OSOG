from idlelib.run import handle_tk_events

import numpy as np
import cv2
from matplotlib import pyplot as plt

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



if __name__ == '__main__':

    cam = cv2.VideoCapture(0)
    im1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    im3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)


    while True:

        #フレーム間差分計算
        im_fs = flame_sub(im1, im2, im3, 5, 7)
        im4 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2BGRA)

        ret,thresh = cv2.threshold(im_fs,127,255,0)
        cnt,im , _ = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
        x,y,w,h = cv2.boundingRect(cnt)
        new_w = h if h > w else w
        new_h = w if w > h else h
        # new_x = x - (int(new_w / 2 - w / 2))
        new_x = x - (new_w - w) // 2 if x > (new_w - w) // 2 else x
        new_y = y - (new_h - h) // 2 if y > (new_h - h) // 2 else y
        #cv2.rectangle(im4, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.rectangle(im4, (new_x, new_y), (new_x + new_w, new_y + new_h), (0, 255, 0), 2)
        dst = im4[new_y:new_y + new_h, new_x:new_x + new_w]
        cv2.imwrite('dst.jpg', dst)

        #識別機にわたすとこやでー




        #識別機からもらうでー



        cv2.imshow("Input", im4)
        cv2.imshow("Motion Mask", im_fs)

        im1 = im2
        im2 = im3
        im3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

# －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ここまで
        key = cv2.waitKey(10)


        #Escキーが押されたら
        if key == 27:
            cv2.destroyAllWindows()
            break
