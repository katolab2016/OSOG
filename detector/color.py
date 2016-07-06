import cv2
import numpy as np

def hsv(cap):

    ret, frame = cap.read()
    #HSV空間に変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_brown = np.array([2, 61, 130])
    upper_brown = np.array([11, 96, 255])

    #指定色のマスク画像
    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    mask = cv2.medianBlur(mask, 7)

    return mask


