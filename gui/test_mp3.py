# -*- coding: utf-8 -*-
#音を再生する
#alarmは警告音
#selectは設定反映時の確認音
import pygame.mixer
import time

# メイン
def alarm(flag = 6):
    if flag == 6:
        name = "keihou_alart.mp3"
    elif flag == 7:
        name = "dedeen.mp3"
    elif flag == 8:
        name = "MGSalarm.mp3"
    elif flag == 9:
        name = "newtype.mp3"
    elif flag == 10:
        name = "nelnel.mp3"

    pygame.mixer.init(frequency = 44100)    # 初期設定
    pygame.mixer.music.load(name)     # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)              # 音楽の再生回数(1回)
    time.sleep(2)                         # 音楽の再生時間
    pygame.mixer.music.stop()               # 再生の終了

def select():
    pygame.mixer.init(frequency=44100)  # 初期設定
    pygame.mixer.music.load("open.mp3")  # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)  # 音楽の再生回数(1回)
    time.sleep(2)  # 音楽の再生時間
    pygame.mixer.music.stop()

if __name__ == '__main__':
    alarm()
