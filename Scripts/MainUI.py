import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

from TierList import TierWindowUI
from PlayerRecord import RecordFrameUI
from ingameinfo import Ui_MainWindow as InGameInfoUI
import Resources_rc

sys.path.append(os.path.join(os.path.dirname(__file__), 'Scripts'))
#from UITest import ImgSelectUI

MainUiSource = uic.loadUiType("Data/UI/MainUI/main.ui")[0]

class MainUI(QWidget, MainUiSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.isDragbarClicked = False

        self.ui1 = TierWindowUI()

        self.ui2 = RecordFrameUI()
        self.ui3= QMainWindow()

        self.MainWindow.addWidget(self.ui1)
        self.MainWindow.addWidget(self.ui2)
        self.MainWindow.addWidget(self.ui3)

        self.MinimizeButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.ExitButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.TierListButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.MatchRecordButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.InGameMMRButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.MinimizeButton.clicked.connect(self.Minimize_Window)
        self.ExitButton.clicked.connect(self.Quit_Window)
        self.TierListButton.clicked.connect(lambda: self.display(1))
        self.MatchRecordButton.clicked.connect(lambda: self.display(2))
        self.InGameMMRButton.clicked.connect(lambda: self.display(3))
        
        self.TierListButton.setChecked(True)
        self.display(1)

    def display(self, index):
        self.MainWindow.setCurrentIndex(index)

    def Minimize_Window(self):
        self.showMinimized()

    def Maximize_Window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def Quit_Window(self):
        self.close()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUI = MainUI()
    mainUI.show()
    sys.exit(app.exec_())