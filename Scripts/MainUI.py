import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSystemTrayIcon
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QIcon
#add library
from MainHotkey import HotkeyListener
#
from TierList import TierWindowUI
from PlayerRecord import RecordFrameUI
from MMRUI import MMRWindowUI
from UITest import ImgSelectUI, CaptureHelperUI
import Resources_rc
import champIcons_rc
#
from OCR.Scripts.NicknameOCR import NicknameCapture


MainUiSource = uic.loadUiType("Data/UI/MainUI/Main.ui")[0]

class MainUI(QWidget, MainUiSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ER.GG")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.Icon = QIcon("Data/UI/UIResource/CharIcon/238.png")
        self.setWindowIcon(self.Icon)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setIcon(self.Icon)

        self.isDragbarClicked = False

        self.ui1 = TierWindowUI()

        self.ui2 = RecordFrameUI()

        self.ui3 = MMRWindowUI()

        self.ui4 = ImgSelectUI()

        self.ocr = NicknameCapture()

        self.MainWindow.addWidget(self.ui1)
        self.MainWindow.addWidget(self.ui2)
        self.MainWindow.addWidget(self.ui3)

        self.MinimizeButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ExitButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.CaptureButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.TierListButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.MatchRecordButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.InGameMMRButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.MinimizeButton.clicked.connect(self.Minimize_Window)
        self.ExitButton.clicked.connect(self.Quit_Window)
        self.CaptureButton.clicked.connect(self.Capture_Window)

        self.TierListButton.clicked.connect(lambda: self.display(1))
        self.MatchRecordButton.clicked.connect(lambda: self.display(2))
        self.InGameMMRButton.clicked.connect(lambda: self.display(3))
        
        self.TierListButton.setChecked(True)
        self.display(1)
        
    #############################
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.hotkey_pressed.connect(self.HotKeyEvent)
        self.hotkey_listener.start()
    #############################    

    def display(self, index):
        self.MainWindow.setCurrentIndex(index)
        
        if index == 1:
            self.TierListButton.setChecked(True)
            self.MatchRecordButton.setChecked(False)
            self.InGameMMRButton.setChecked(False)
        elif index == 2:
            self.TierListButton.setChecked(False)
            self.MatchRecordButton.setChecked(True)
            self.InGameMMRButton.setChecked(False)
        elif index == 3:
            self.TierListButton.setChecked(False)
            self.MatchRecordButton.setChecked(False)
            self.InGameMMRButton.setChecked(True)

    def Minimize_Window(self):
        self.showMinimized()
    
    def Show_Window(self):
        self.showNormal()
        self.activateWindow()

    def Maximize_Window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def Quit_Window(self):
        self.close()

    def Capture_Window(self):
        self.ui4.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.pos().y() <= self.DragBar.height():
            self.isDragbarClicked = True
            self.oldPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.pos().y() <= self.DragBar.height() and self.isDragbarClicked == True:
            self.isDragbarClicked = False
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and event.pos().y() <= self.DragBar.height() and self.isDragbarClicked:  
            self.move(event.globalPos() - self.oldPos)
            event.accept()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # 아이콘 클릭 이벤트
            if self.isVisible():
                self.hide()
            else:
                self.Show_Window()

    def HotKeyEvent(self): 
        self.Show_Window()
        self.display(3)
        nameList = self.ocr.OCR_Nickname()
        self.ui3.UpdateData(nameList)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUI = MainUI()
    mainUI.show()
    sys.exit(app.exec_())