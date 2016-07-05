# -*- coding: UTF-8 -*-
#設定を受け取ってGがいた画像の表示
import cv2

def mosaic(flag_graph = 2):
    #画像を読み込む(サンプルの設定になってます)
    img_src = cv2.imread("IMG_20160522_194947.JPG", 1)

    # 元の画像のサイズを取得
    size = img_src.shape[:2][::-1]

    # 画像全体を一度1/20に縮小
    img_tmp = cv2.resize(img_src, (int(size[0] / 10), int(size[1] / 10)))

    # 圧縮したものを再度元のサイズに拡大
    img_dst = cv2.resize(img_tmp, size, interpolation=cv2.INTER_NEAREST)

    # 表示
    if flag_graph == 1:
        #生画像表示
        cv2.imshow("Original_G", img_src)
    elif flag_graph == 2:
        #モザイク画像表示
        cv2.imshow("Mosaic_G", img_dst)
    else :
        #新たに規制ステッカを読み込んで表示
        img_irst = cv2.imread("G_st.JPG", 1)
        cv2.imshow("Image_G", img_irst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    mosaic()