# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'practice3.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PlayerInfo():
    BlueorRed = False
    playerName = "nickname"
    playerSpell1 = "positionD"
    playerSpell2 = "positionF"
    playerKill = "playerkill"
    playerDeath = "playerdeath"
    playerAssist = "playerassist"
    playerMainRune = "playermainrune"
    playerSubRune = "playersubrune"
    playerMiniRune = "playerminirune"
    playerTier = "playertier"
    playerLane = "playerlane"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(53, 52, 61);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 10, 1920, 1080))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setStyleSheet("border: none;")
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 960, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Bteam = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Bteam.setStyleSheet("color: white;")
        self.Bteam.setObjectName("Bteam")
        self.verticalLayout.addWidget(self.Bteam)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(955, 0, 960, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Rteam = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.Rteam.setStyleSheet("color: white;")
        self.Rteam.setObjectName("Rteam")
        self.verticalLayout_2.addWidget(self.Rteam)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 80, 374, 70))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Bchamp = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.Bchamp.setStyleSheet("color: rgb(198, 198, 198);")
        self.Bchamp.setObjectName("Bchamp")
        self.verticalLayout_3.addWidget(self.Bchamp)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(373, 80, 404, 70))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Brune = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.Brune.setStyleSheet("color: rgb(198, 198, 198);")
        self.Brune.setObjectName("Brune")
        self.verticalLayout_4.addWidget(self.Brune)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(1545, 80, 374, 70))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Rchamp = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.Rchamp.setStyleSheet("color: rgb(198, 198, 198);")
        self.Rchamp.setObjectName("Rchamp")
        self.verticalLayout_5.addWidget(self.Rchamp)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(1141, 80, 404, 70))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Rrune = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.Rrune.setStyleSheet("color: rgb(198, 198, 198);")
        self.Rrune.setObjectName("Rrune")
        self.verticalLayout_6.addWidget(self.Rrune)
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(776, 80, 364, 70))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lane = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.lane.setStyleSheet("color: rgb(198, 198, 198);")
        self.lane.setObjectName("lane")
        self.verticalLayout_7.addWidget(self.lane)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 150, 373, 186))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.Bchamp1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Bchamp1.setContentsMargins(0, 0, 1, 0)
        self.Bchamp1.setObjectName("Bchamp1")
        self.blueTop = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.blueTop.setStyleSheet("color: rgb(255, 255, 255);")
        self.blueTop.setObjectName("blueTop")
        self.Bchamp1.addWidget(self.blueTop)

        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(374, 150, 403, 186))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 1, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label)

        # 이미지 가로 정렬을 위해 horizontalBoxLayout으로 변경
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(778, 160, 363, 186))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_13")
        self.verticalLayout_9 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_9.setContentsMargins(0, 0, 1, 0)
        self.verticalLayout_9.setAlignment(Qt.AlignCenter)
        self.verticalLayout_9.setObjectName("verticalLayout_13")

        ###티어 이미지 로드하는 곳###
        self.tier0 = QPixmap("imagefile/bronze.png")
        self.tier1 = QPixmap("imagefile/silver.png")
        self.tier2 = QPixmap("imagefile/gold.png")
        self.tier3 = QPixmap("imagefile/platinum.png")
        self.tier4 = QPixmap("imagefile/diamond.png")
        self.tier5 = QPixmap("imagefile/master.png")
        self.tier6 = QPixmap("imagefile/grandmaster.png")
        self.tier7 = QPixmap("imagefile/challenger.png")

        ###라인 이미지 로드하는 곳###
        self.toplane = QPixmap("imagefile/TOP.png")
        self.juglane = QPixmap("imagefile/JUG.png")
        self.midlane = QPixmap("imagefile/MID.png")
        self.botlane = QPixmap("imagefile/BOT.png")
        self.suplane = QPixmap("imagefile/SUP.png")

        ###json 파일에서 읽어온 정보를 토대로 맞는 사진을 로드한다 top 위치###
        self.toptierimage = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.toptierimage.setPixmap(self.tier7.scaled(100, 100))
        # 라인 이미지
        self.toplaneimage = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.toplaneimage.setPixmap(self.toplane.scaled(60, 60))
        self.toplaneimage.setContentsMargins(20, 0, 20, 0)
        # 상대 티어
        self.etoptierimage = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.etoptierimage.setPixmap(self.tier3.scaled(100, 100))
        self.verticalLayout_9.addWidget(self.toptierimage)
        self.verticalLayout_9.addWidget(self.toplaneimage)
        self.verticalLayout_9.addWidget(self.etoptierimage)

        # jungle 위치
        self.Widgetjugtier = QtWidgets.QWidget(self.frame)
        self.Widgetjugtier.setGeometry(QtCore.QRect(778, 346, 363, 186))
        self.jugtier = QtWidgets.QHBoxLayout(self.Widgetjugtier)
        self.jugtier.setAlignment(Qt.AlignCenter)
        self.jugtierimage = QtWidgets.QLabel(self.Widgetjugtier)
        self.jugtierimage.setPixmap(self.tier6.scaled(100, 100))
        # 라인 이미지
        self.juglaneimage = QtWidgets.QLabel(self.Widgetjugtier)
        self.juglaneimage.setPixmap(self.juglane.scaled(60, 60))
        self.juglaneimage.setContentsMargins(20, 0, 20, 0)
        # 상대 티어
        self.ejugtierimage = QtWidgets.QLabel(self.Widgetjugtier)
        self.ejugtierimage.setPixmap(self.tier4.scaled(100, 100))
        self.jugtier.addWidget(self.jugtierimage)
        self.jugtier.addWidget(self.juglaneimage)
        self.jugtier.addWidget(self.ejugtierimage)

        # mid 위치
        self.Widgetmidtier = QtWidgets.QWidget(self.frame)
        self.Widgetmidtier.setGeometry(QtCore.QRect(778, 532, 363, 186))
        self.midtier = QtWidgets.QHBoxLayout(self.Widgetmidtier)
        self.midtier.setAlignment(Qt.AlignCenter)
        self.midtierimage = QtWidgets.QLabel(self.Widgetmidtier)
        self.midtierimage.setPixmap(self.tier5.scaled(100, 100))
        # 라인 이미지
        self.midlaneimage = QtWidgets.QLabel(self.Widgetmidtier)
        self.midlaneimage.setPixmap(self.midlane.scaled(60, 60))
        self.midlaneimage.setContentsMargins(20, 0, 20, 0)
        # 상대 티어
        self.emidtierimage = QtWidgets.QLabel(self.Widgetmidtier)
        self.emidtierimage.setPixmap(self.tier5.scaled(100, 100))
        self.midtier.addWidget(self.midtierimage)
        self.midtier.addWidget(self.midlaneimage)
        self.midtier.addWidget(self.emidtierimage)

        # AD 위치
        self.WidgetADtier = QtWidgets.QWidget(self.frame)
        self.WidgetADtier.setGeometry(QtCore.QRect(778, 718, 363, 186))
        self.ADtier = QtWidgets.QHBoxLayout(self.WidgetADtier)
        self.ADtier.setAlignment(Qt.AlignCenter)
        self.ADtierimage = QtWidgets.QLabel(self.WidgetADtier)
        self.ADtierimage.setPixmap(self.tier4.scaled(100, 100))
        # 라인 이미지
        self.botlaneimage = QtWidgets.QLabel(self.WidgetADtier)
        self.botlaneimage.setPixmap(self.botlane.scaled(60, 60))
        self.botlaneimage.setContentsMargins(20, 0, 20, 0)
        # 상대 티어
        self.eADtierimage = QtWidgets.QLabel(self.WidgetADtier)
        self.eADtierimage.setPixmap(self.tier6.scaled(100, 100))
        self.ADtier.addWidget(self.ADtierimage)
        self.ADtier.addWidget(self.botlaneimage)
        self.ADtier.addWidget(self.eADtierimage)

        # SUP 위치
        self.Widgetsuptier = QtWidgets.QWidget(self.frame)
        self.Widgetsuptier.setGeometry(QtCore.QRect(778, 904, 363, 186))
        self.suptier = QtWidgets.QHBoxLayout(self.Widgetsuptier)
        self.suptier.setAlignment(Qt.AlignCenter)
        self.suptierimage = QtWidgets.QLabel(self.Widgetsuptier)
        self.suptierimage.setPixmap(self.tier3.scaled(100, 100))
        # 라인 이미지
        self.suplaneimage = QtWidgets.QLabel(self.Widgetsuptier)
        self.suplaneimage.setPixmap(self.suplane.scaled(60, 60))
        self.suplaneimage.setContentsMargins(20, 0, 20, 0)
        # 상대 티어
        self.esuptierimage = QtWidgets.QLabel(self.Widgetsuptier)
        self.esuptierimage.setPixmap(self.tier7.scaled(100, 100))
        self.suptier.addWidget(self.suptierimage)
        self.suptier.addWidget(self.suplaneimage)
        self.suptier.addWidget(self.esuptierimage)

        self.verticalLayoutWidget_10 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_10.setGeometry(QtCore.QRect(1142, 150, 403, 186))
        self.verticalLayoutWidget_10.setObjectName("verticalLayoutWidget_18")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_10.setContentsMargins(0, 0, 1, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_18")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_10.addWidget(self.label_3)
        self.verticalLayoutWidget_11 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_11.setGeometry(QtCore.QRect(1546, 150, 373, 186))
        self.verticalLayoutWidget_11.setObjectName("verticalLayoutWidget_19")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_11.setContentsMargins(0, 0, 1, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_19")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_11)
        self.label_4.setStyleSheet("color: rgb(255,255,255);")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Bteam.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">블루팀</span></p></body></html>"))
        self.Rteam.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">레드팀 </span></p></body></html>"))
        self.Bchamp.setText(_translate("MainWindow",
                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Champion</span></p></body></html>"))
        self.Brune.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Rune</p></body></html>"))
        self.Rchamp.setText(_translate("MainWindow",
                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Champion</span></p></body></html>"))
        self.Rrune.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Rune</span></p></body></html>"))
        self.lane.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">lane</span></p></body></html>"))
        self.blueTop.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">imported champion info</p></body></html>"))
        self.label.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">imported used rune</p></body></html>"))
        self.label_3.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">opponent rune</p></body></html>"))
        self.label_4.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">opponent champion</p></body></html>"))

    def initialize(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.initialize()  # 추가된 초기화 메서드 호출
    MainWindow.show()
    sys.exit(app.exec_())