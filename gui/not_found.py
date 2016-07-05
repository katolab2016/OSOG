# -*- coding: UTF-8 -*-
#Gが検知できなかった時に画像を表示する
import cv2

def no_G_show():
    img_src = cv2.imread("not_G.JPG", 1)

    cv2.imshow("G is not found", img_src)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    no_G_show()