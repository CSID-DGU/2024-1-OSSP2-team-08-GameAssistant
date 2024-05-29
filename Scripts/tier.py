import sys
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

class TierUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initialize()

    def setupUi(self):
        window_height = 720
        window_width = 1280

        self.setWindowTitle("Tier")
        self.setGeometry(0, 0, window_width, window_height)
        self.setStyleSheet("background-color: #19191A;")

        icon_x = 10
        icon_y = 60
        icon_button_width = 60
        icon_button_height = 60
        icon_label_width = 60
        icon_label_height = 20
        tier_x = 10
        tier_y = 45

        icons_folder = '.\\JH\\c_icons\\champ_icons'
        icon_files = os.listdir(icons_folder)
        icon_path = []
        for icon_file in icon_files:
            icon_path.append(os.path.join(icons_folder, icon_file))
        icon_path.sort()

        tier_icon_folder = '.\\JH\\c_icons\\tier_icons'
        tier_icon_files = os.listdir(tier_icon_folder)
        tier_icon_path = []
        for tier_icon_file in tier_icon_files:
            tier_icon_path.append(os.path.join(tier_icon_folder, tier_icon_file))

        file = open('./Data/TestJson/championTier/champion.json', 'r', encoding='utf-8')
        c_file = json.load(file)
        self.c_lists = [[] for i in range(c_file["data"].__len__())]
        i = 0
        tier = 0
        for data in c_file["data"]:
            self.c_lists[i].append(c_file["data"][data]["name"])
            self.c_lists[i].append(c_file["data"][data]["Winrate"])
            self.c_lists[i].append(c_file["data"][data]["Pickrate"])
            self.c_lists[i].append(c_file["data"][data]["Banrate"])
            if self.c_lists[i][1] >= 55.0:
                tier = 0
            elif 55.0 > self.c_lists[i][1] >= 52.0:
                tier = 1
            elif 52.0 > self.c_lists[i][1] >= 50.0:
                tier = 2
            elif 50.0 > self.c_lists[i][1] >= 48.0:
                tier = 3
            elif 48.0 > self.c_lists[i][1] >= 45.0:
                tier = 4
            elif 45.0 > self.c_lists[i][1]:
                tier = 5
            self.c_lists[i].append(tier)
            i += 1

        scroll_area_1 = QScrollArea(self)
        scroll_area_1.setGeometry(120, 100, 300, 600)
        scroll_area_1.setWidgetResizable(True)
        scroll_area_1.viewport().setStyleSheet("background-color: #201F22;")
        scroll_content_1 = QWidget()
        scroll_area_1.setWidget(scroll_content_1)
        scroll_area_1.setStyleSheet("background-color: #201F22;"
                                    "border-width: 0px;"
                                    "border-radius: 15px;")

        # 우하단 영역
        scroll_area_2 = QScrollArea(self)
        scroll_area_2.setGeometry(432, 100, 480, 600)
        scroll_area_2.setWidgetResizable(True)
        scroll_area_2.viewport().setStyleSheet("background-color: #201F22;")
        scroll_content_2 = QWidget()
        scroll_area_2.setWidget(scroll_content_2)
        scroll_area_2.setStyleSheet("background-color: #201F22;"
                                    "border-width: 0px;"
                                    "border-radius: 15px;")

        # 상단 영역
        scroll_area_3 = QScrollArea(self)
        scroll_area_3.setGeometry(120, 20, 792, 70)
        scroll_area_3.setWidgetResizable(True)
        scroll_area_3.viewport().setStyleSheet("background-color: #201F22;")
        scroll_content_3 = QWidget()
        scroll_area_3.setWidget(scroll_content_3)
        scroll_area_3.setStyleSheet("background-color: #201F22;"
                                    "border-width: 0px;"
                                    "border-radius: 15px;")

        # 아이콘 검색창
        self.lineEdit = QLineEdit(scroll_content_1)
        self.lineEdit.setGeometry(10, 10, 280, 40)
        self.lineEdit.setStyleSheet("background-color: #2B2B30;"
                                    "border-width: 0px;"
                                    "border-radius: 3px;")
        self.lineEdit.textChanged.connect(self.filterButtons)

        self.icon_buttons = []
        self.icon_labels = []
        for j in range(icon_path.__len__()):
            button = QPushButton(scroll_content_1)
            button.setIcon(QIcon(icon_path[j]))
            button.setIconSize(QtCore.QSize(icon_button_width, icon_button_height))
            button.setGeometry(icon_x, icon_y, icon_button_width, icon_button_height)
            button.setObjectName(f"Icon_{str(icon_files[j][:-4])}")
            button.setText("")  # 버튼 텍스트 제거
            self.icon_buttons.append(button)

            label = QLabel(f"Label {j + 1}", scroll_content_1)
            label.setText(icon_files[j][:-4])
            label.setObjectName(f"Label {j + 1}")
            if len(icon_files[j][:-4]) > 3:
                label.setText((str(icon_files[j][:3]) + "..."))
            label.setGeometry(icon_x, icon_y + 60, icon_label_width, icon_label_height)
            label.setStyleSheet("color: #9E9EAF;")
            self.icon_labels.append(label)
            if j % 4 == 3:
                icon_x = 10
                icon_y += 90
            else:
                icon_x += 70

        self.tier_buttons = []
        self.tier_labels = []
        for i in range(self.c_lists.__len__()):
            button_2a = QPushButton(scroll_content_2)
            for j in range(icon_path.__len__()):
                if str(self.c_lists[i][0]) in icon_path[j]:
                    button_2a.setIcon(QIcon(icon_path[j]))
            button_2a.setIconSize(QtCore.QSize(45, 45))
            button_2a.setGeometry(tier_x, tier_y, 50, 50)
            button_2a.setObjectName(f"Tier_icon_{str(self.c_lists[i][0])}")
            button_2a.setText("")

            button_2b = QPushButton(scroll_content_2)
            button_2b.setIcon(QIcon(tier_icon_path[self.c_lists[i][4]]))
            button_2b.setIconSize(QtCore.QSize(45, 45))
            button_2b.setGeometry(tier_x + 50, tier_y, 50, 50)
            button_2b.setObjectName(f"Tier_tier_{str(self.c_lists[i][0])}")
            button_2b.setText("")

            label_2a = QLabel(scroll_content_2)
            label_2a.setGeometry(tier_x + 100, tier_y, 60, 50)
            label_2a.setText(str(self.c_lists[i][0]))
            if (len(str(self.c_lists[i][0])) > 3):
                label_2a.setText(str(self.c_lists[i][0][:3]) + "...")
            label_2a.setStyleSheet("color: #9E9EAF;")

            label_2b = QLabel(scroll_content_2)
            label_2b.setGeometry(tier_x + 180, tier_y, 50, 50)
            label_2b.setText(str(self.c_lists[i][1]) + "%")
            label_2b.setStyleSheet("color: #9E9EAF;")

            label_2c = QLabel(scroll_content_2)
            label_2c.setGeometry(tier_x + 250, tier_y, 50, 50)
            label_2c.setText(str(self.c_lists[i][2]) + "%")
            label_2c.setStyleSheet("color: #9E9EAF;")

            label_2d = QLabel(scroll_content_2)
            label_2d.setGeometry(tier_x + 320, tier_y, 50, 50)
            label_2d.setText(str(self.c_lists[i][3]) + "%")
            label_2d.setStyleSheet("color: #9E9EAF;")

            self.tier_buttons.append([button_2a, button_2b])
            self.tier_labels.append([label_2a, label_2b, label_2c, label_2d])
            tier_y += 55

        self.button1 = QPushButton(scroll_content_2)
        self.button1.setObjectName("TierSort")
        self.button1.setText("티어")
        self.button1.setStyleSheet("color: #9E9EAF;"
                                   "border-width: 0px;"
                                   "border-radius: 3px;")
        self.button1.setGeometry(60, 0, 50, 50)
        self.button1.clicked.connect(lambda:self.sortTiers(4))

        self.button2 = QPushButton(scroll_content_2)
        self.button2.setObjectName("NameSort")
        self.button2.setText("이름")
        self.button2.setStyleSheet("color: #9E9EAF;"
                                   "border-width: 0px;"
                                   "border-radius: 3px;")
        self.button2.setGeometry(115, 0, 50, 50)
        self.button2.clicked.connect(lambda:self.sortTiers(0))

        self.button3 = QPushButton(scroll_content_2)
        self.button3.setObjectName("WRSort")
        self.button3.setText("승률")
        self.button3.setStyleSheet("color: #9E9EAF;"
                                   "border-width: 0px;"
                                   "border-radius: 3px;")
        self.button3.setGeometry(185, 0, 50, 50)
        self.button3.clicked.connect(lambda:self.sortTiers(1))

        self.button4 = QPushButton(scroll_content_2)
        self.button4.setObjectName("PRSort")
        self.button4.setText("픽율")
        self.button4.setStyleSheet("color: #9E9EAF;"
                                   "border-width: 0px;"
                                   "border-radius: 3px;")
        self.button4.setGeometry(255, 0, 50, 50)
        self.button4.clicked.connect(lambda:self.sortTiers(2))

        self.button5 = QPushButton(scroll_content_2)
        self.button5.setObjectName("BRSort")
        self.button5.setText("밴율")
        self.button5.setStyleSheet("color: #9E9EAF;"
                                   "border-width: 0px;"
                                   "border-radius: 3px;")
        self.button5.setGeometry(325, 0, 50, 50)
        self.button5.clicked.connect(lambda:self.sortTiers(3))

    def initialize(self):
        pass

    def filterButtons(self, text):
        text = text.replace(" ", "")
        x = 10
        y = 50
        i = 0
        for button, label in zip(self.icon_buttons, self.icon_labels):
            if text not in button.objectName():
                button.hide()
                label.hide()
                button.setDisabled(True)
                label.setDisabled(True)
            else:
                button.show()
                label.show()
                button.setEnabled(True)
                label.setEnabled(True)
                button.setGeometry(x, y, 60, 60)
                label.setGeometry(x, y + 60, 60, 20)
                if (i + 1) % 4 == 0:
                    y += 80
                    x = 10
                else:
                    x += 70
                i += 1

    def sortTiers(self, num):
        x = 10
        y = 45
        self.c_lists.sort(key = lambda x: x[num])
        if num != 4 and num != 0:
            self.c_lists.reverse()
        for i in range(self.c_lists.__len__()):
            for button, label in zip(self.tier_buttons, self.tier_labels):
                if self.c_lists[i][0] in button[0].objectName():
                    button[0].setGeometry(x, y, 50, 50)
                    button[1].setGeometry(x + 50, y, 50, 50)
                    label[0].setGeometry(x + 100, y, 50, 50)
                    label[1].setGeometry(x + 180, y, 50, 50)
                    label[2].setGeometry(x + 250, y, 50, 50)
                    label[3].setGeometry(x + 320, y, 50, 50)
            y += 55

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()
    sys.exit(app.exec_())