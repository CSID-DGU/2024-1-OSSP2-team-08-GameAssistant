import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5 import QtCore

from main import UI_MainWindow
from PlayerRecord import RecordFrameUI
from ingameinfo import Ui_MainWindow as InGameInfoUI

sys.path.append(os.path.join(os.path.dirname(__file__), 'Scripts'))
#from UITest import ImgSelectUI

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.oldPos = self.pos()
        self.initUI()

    def initUI(self):

        windowSpace = 200
        windowWidth = 1600 - windowSpace
        windowHeight = 800
        uiHeight = 800
        uiWidth = 1400 - windowSpace

        self.setWindowTitle('Multi UI Example')
        self.setGeometry(100, 100, windowWidth, windowHeight)

        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("background-color: gray;")

        btn_Maximize = QPushButton("ㅁ", self.title_bar)
        btn_Minimize = QPushButton('-', self.title_bar)
        btn_Quit = QPushButton("X", self.title_bar)

        btn_Maximize.setFixedHeight(50)
        btn_Minimize.setFixedHeight(50)
        btn_Quit.setFixedHeight(50)
        btn_Maximize.setFixedWidth(50)
        btn_Minimize.setFixedWidth(50)
        btn_Quit.setFixedWidth(50)

        btn_Maximize.clicked.connect(self.Maximize_Window)
        btn_Minimize.clicked.connect(self.Minimize_Window)
        btn_Quit.clicked.connect(self.Quit_Window)

        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(btn_Minimize)
        title_bar_layout.addWidget(btn_Maximize)
        title_bar_layout.addWidget(btn_Quit)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFixedHeight(uiHeight)
        self.stacked_widget.setFixedWidth(uiWidth)

        self.ui1 = UI_MainWindow()
        self.ui1.initialize()

        self.ui2 = self.load_player_record_ui()
        self.ui2.initialize()

        self.ui3, self.ui3_widget = self.load_ingame_info_ui()
        self.ui3_widget.initialize()

        self.ui4 = self.load_img_select_ui()
        self.ui4.initialize()

        self.stacked_widget.addWidget(self.ui1)
        self.stacked_widget.addWidget(self.ui2)
        self.stacked_widget.addWidget(self.ui3)
        self.stacked_widget.addWidget(self.ui4)

        self.btn1 = QPushButton("main.py")
        self.btn2 = QPushButton("PlayerRecord.py")
        self.btn3 = QPushButton("ingameinfo.py")
        self.btn4 = QPushButton("UITest.py")

        self.btn1.clicked.connect(lambda: self.display(0))
        self.btn2.clicked.connect(lambda: self.display(1))
        self.btn3.clicked.connect(lambda: self.display(2))
        self.btn4.clicked.connect(lambda: self.display(3))

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn1)
        button_layout.addWidget(self.btn2)
        button_layout.addWidget(self.btn3)
        button_layout.addWidget(self.btn4)
        button_layout.addStretch(1)

        central_layout = QHBoxLayout()
        spacer_left = QSpacerItem(windowSpace, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(windowSpace, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        central_layout.addItem(spacer_left)
        central_layout.addWidget(self.stacked_widget)
        central_layout.addItem(spacer_right)

        content_layout = QHBoxLayout()
        content_layout.addLayout(button_layout)
        content_layout.addLayout(central_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(content_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setLayout(main_layout)
        self.update_button_styles(0)

    def load_player_record_ui(self):
        ui = RecordFrameUI()
        return ui

    def load_ingame_info_ui(self):
        ui = QMainWindow()
        ui_widget = InGameInfoUI()
        ui_widget.setupUi(ui)
        return ui, ui_widget

    def load_img_select_ui(self):
        ui = ImgSelectUI()
        return ui

    def display(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.update_button_styles(index)

    def update_button_styles(self, active_index):
        buttons = [self.btn1, self.btn2, self.btn3, self.btn4]
        for i, btn in enumerate(buttons):
            if i == active_index:
                btn.setStyleSheet("background-color: lightblue;")
            else:
                btn.setStyleSheet("background-color: none;")

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