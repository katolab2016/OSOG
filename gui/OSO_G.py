#メインで動かすGUIのファイル
#設定1,a：画像表示（無修正）
#設定2,b：画像表示(モザイク)
#設定3,c：ステッカー規制

#設定4,d：警告音アリ
#設定5,e：警告音なし
#ユーザにはラジオボタンを提示(画像、音で1つずつの選択)
#反映ボタンを押したときにその設定を反映
# -*- coding:utf-8 -*-

import cv2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from osog.gui.save_data import save #設定の保存(get_data.pyの出力)
from osog.gui.mosaic import mosaic #設定を受け取って結果の画像を出力
from osog.gui.not_found import no_G_show #G未検出時の出力
from osog.detector.capture import GDetector
global flag_graph #結果の画像の設定 1:無修正 2:モザイク 3:完全規制ステッカ
global flag_sound #警告音の設定 4:警告音あり 5:無音
global result #結果のフラグ　0:G検出、1:未検出
global wanted_pic   #結果の画像
# from data import get_data
from osog.gui.set_data import set_data #前回設定の読み込み
from osog.gui.test_mp3 import alarm, select #alarm:警告音　select:設定反映時の音出力
import sys
dbg = 1  # 1:debugモード, 0:nomal


class Setting(QWidget):
    def __init__(self, parent=None):
        super(Setting, self).__init__(parent)
        self.lineLayout = QGridLayout()
        self.myVLayout = QVBoxLayout()

        #反映ボタン
        self.reflectButton = QPushButton("&設定を反映")
        self.reflectButton.clicked.connect(self.reflect)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.reflectButton)
        #項目のテキスト
        self.lineLayout.addWidget(QLabel("画像表示 :"), 0, 0)
        self.lineLayout.addWidget(QLabel("警告音 :"), 1, 0)
        # ラジオボタンA 無修正
        self.radio_a = QRadioButton('無修正')
        self.lineLayout.addWidget(self.radio_a, 0, 1)
        # ラジオボタンB モザイク加工
        self.radio_b = QRadioButton('モザイク加工')
        self. lineLayout.addWidget(self.radio_b, 0, 2)
        # ラジオボタンC 画像無し
        self.radio_c = QRadioButton('画像無し')
        self.lineLayout.addWidget(self.radio_c, 0, 3)
        # ラジオボタンD 警告音アリ
        self.radio_d = QRadioButton('警告音あり')
        self.lineLayout.addWidget(self.radio_d, 1, 1)
        # ラジオボタンE 無音
        self.radio_e = QRadioButton('無音')
        self.lineLayout.addWidget(self.radio_e, 1, 2)
        # 画像表示に関するラジオボタンのグループ
        self.group_a = QButtonGroup()
        self.group_a.addButton(self.radio_a, 1)
        self.group_a.addButton(self.radio_b, 2)
        self.group_a.addButton(self.radio_c, 3)
        # 警告音に関するラジオボタンのグループ
        self.group_b = QButtonGroup()
        self.group_b.addButton(self.radio_d, 4)
        self.group_b.addButton(self.radio_e, 5)

        self.myVLayout.addLayout(self.lineLayout)
        self.myVLayout.addLayout(buttonLayout)
        self.setLayout(self.myVLayout)

    def reflect(self):
        global flag_graph
        global flag_sound
        #それぞれのラジオボタンをチェックしてフラグ保存
        if self.radio_a.isChecked():
            flag_graph = 1
        elif self.radio_b.isChecked():
            flag_graph = 2
        elif self.radio_c.isChecked():
            flag_graph = 3

        if self.radio_d.isChecked():
            flag_sound = 4
        elif self.radio_e.isChecked():
            flag_sound = 5
        #警告音の設定を反映した時に音を再生
        if flag_sound == 4:
            select()
        #設定を関数を定義したファイルとして保存
        save(flag_graph, flag_sound)

    def retranslateUi(self, NewWindow): #ウィンドウタイトルの変更を行う
        NewWindow.setObjectName("NewWindow")
        _translate = QtCore.QCoreApplication.translate
        NewWindow.setWindowTitle(_translate("Newwindow", "設定"))
        QtCore.QMetaObject.connectSlotsByName(NewWindow)

class MainMenu(QWidget):
    def __init__(self, sysarg, parent=None):
        app = QApplication(sysarg)
        super(MainMenu, self).__init__(parent)
        HLayout = QHBoxLayout()
        self.VLayout = QVBoxLayout()
        resultVLayout = QVBoxLayout()
        # 画像表示に関する部分
        self.imageLabel = QLabel()
        image = QtGui.QImage()
        image.load("Screen Shot 2016-05-10 at 2.28.02 PM.png")
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image)
        self.imageLabel.setPixmap(pixmap)
        #ボタンと関数の関連付け
        self.resultBtn = QPushButton("&結果を確認")
        self.resultBtn.clicked.connect(self.result)
        self.settingBtn = QPushButton("&設定を変更")
        self.settingBtn.clicked.connect(self.settingmenu)
        self.resetBtn = QPushButton("&結果をリセット")
        self.resetBtn.clicked.connect(self.reset)

        #検出器まわり
        self.detector = GDetector()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_predict)
        timer.start(1)
        self.text = QLineEdit()
        self.text.setReadOnly(True)

        #レイアウト
        resultVLayout.addWidget(self.resultBtn)
        resultVLayout.addWidget(self.resetBtn)
        resultVLayout.addWidget(self.text)

        HLayout.addLayout(resultVLayout)
        HLayout.addWidget(self.settingBtn)
        # 画像をレイアウトに追加
        self.VLayout.addWidget(self.imageLabel)

        self.VLayout.addLayout(HLayout)

        self.setLayout(self.VLayout)
        #サイズとウィンドウタイトル
        self.setGeometry(500, 500, 200, 100)
        self.setWindowTitle("メインメニュー")

        self.show()
        sys.exit(app.exec_())

    # 設定画面の出力
    def settingmenu(self):
        setting_window = SetWindow()
        setting_window.show()
        setting_window.exec_()

    #結果を画像で表示
    def result(self):
        global flag_graph
        global result
        global wanted_pic
        if result == 0: #Gを検出した時
            mosaic(flag_graph, wanted_pic)  #設定のフラグを渡して画像表示
        else :  #Gを検出できなかった時
            no_G_show() #「検出できなかった」画像を表示

    #リセットボタン(使用しなくてもOK)
    def reset(self):
        global result
        result = 1

    def update_predict(self):
        global result
        global wanted_pic
        global flag_sound
        pic = self.detector.exists()
        if pic[1]:
            result = 0
            wanted_pic = pic[0]
            if flag_sound == 4: #設定で警告音を鳴らす
                alarm()
        self.text.setText(str(result))

#設定画面を出力するための土台を作るクラス
class SetWindow(QDialog):
    def __init__(self):
        super(SetWindow, self).__init__()
        dialog = Setting()
        dialog.__init__(self)
        #dialog.setup(self)
        dialog.setObjectName("Dialog")
        #ウィンドウの大きさ指定
        dialog.resize(350, 150)
        #ウィンドウタイトルを設定
        dialog.retranslateUi(self)
        #self.show()
        #self.exec_()

def main():
    global flag_graph
    global flag_sound
    global result
    if dbg == 1:
        result = 0
    flag_graph, flag_sound = set_data()
    main_window = MainMenu(sys.argv)

if __name__ == '__main__':
#    import sys
    main()
#    global flag_graph
#    global flag_sound
#    global result
#    if dbg == 1:
#        result = 0

#    flag_graph, flag_sound = get_data()
    #app = QApplication(sys.argv)
#    main_window = MainMenu(sys.argv)

    #main_window.show()
    #sys.exit(app.exec_())