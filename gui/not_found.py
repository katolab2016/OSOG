# -*- coding: UTF-8 -*-
#Gが検知できなかった時に画像を表示する
import cv2
import os

def no_G_show():
    img_src = cv2.imread(os.path.join(os.path.dirname(__file__), 'image/not_G.JPG', 1))

    cv2.imshow("G is not found", img_src)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    no_G_show()