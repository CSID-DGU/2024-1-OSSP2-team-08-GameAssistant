import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5 import QtCore, uic

from main import TierWindowUI
from PlayerRecord import RecordFrameUI
from ingameinfo import Ui_MainWindow as InGameInfoUI

MainWindow = uic.loadUiType("MainWindow.ui")[0]

class MainUI(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.oldPos = self.pos()
        self.setupUi(self)

        self.ui1 = TierWindowUI()
        self.ui1.initialize()
        self.ui2 = RecordFrameUI()
        self.ui2.initialize()
        self.ui3, self.ui3_widget = self.load_ingame_info_ui()
        self.ui3_widget.initialize()

        self.pageStack.addWidget(self.ui1)
        self.pageStack.addWidget(self.ui2)
        self.pageStack.addWidget(self.ui3)

        self.Quit.clicked.connect(self.Quit_Window)
        self.Minimize.clicked.connect(self.Minimize_Window)

        self.menuButton01.clicked.connect(lambda: self.display(0))
        self.menuButton02.clicked.connect(lambda: self.display(1))
        self.menuButton03.clicked.connect(lambda: self.display(2))

    def display(self, index):
        self.pageStack.setCurrentIndex(index)
        self.update_button_styles(index)

    def Minimize_Window(self):
        self.showMinimized()

    def Quit_Window(self):
        self.close()

    def load_player_record_ui(self):
        ui = RecordFrameUI()
        return ui

    def load_ingame_info_ui(self):
        ui = QMainWindow()
        ui_widget = InGameInfoUI()
        ui_widget.setupUi(ui)
        return ui, ui_widget

    def update_button_styles(self, active_index):
        buttons = [self.menuButton01, self.menuButton02, self.menuButton03]
        for i, btn in enumerate(buttons):
            if i == active_index:
                btn.setStyleSheet("background-color: rgb(120, 120, 240);")
            else:
                btn.setStyleSheet("background-color: rgb(255, 255, 255);")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.pos().y() <= self.title_bar.height():
            self.oldPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and event.pos().y() <= self.title_bar.height():
            self.move(event.globalPos() - self.oldPos)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUI = MainUI()
    mainUI.show()
    sys.exit(app.exec_())