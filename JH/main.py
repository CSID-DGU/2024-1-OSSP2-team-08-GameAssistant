import sys
import os
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui

class UI_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Tier")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #19191A;")

        icon_x = 10
        icon_y = 60
        icon_button_width = 60
        icon_button_height = 60
        icon_label_width = 60
        icon_label_height = 20

        tier_x = 10
        tier_y = 40

        icons_folder = '.\\c_icons\\champ_icons'
        icon_files = os.listdir(icons_folder)
        icon_path = []
        for icon_file in icon_files:
            icon_path.append(os.path.join(icons_folder, icon_file))
        icon_path.sort()

        tier_icon_folder = '.\\c_icons\\tier_icons'
        tier_icon_files = os.listdir(tier_icon_folder)
        tier_icon_path = []
        for tier_icon_file in tier_icon_files:
            tier_icon_path.append(os.path.join(tier_icon_folder, tier_icon_file))

        tier_folder = '.\\c_prop'
        tier_files = os.listdir(tier_folder)
        tier_path = []
        for tier_file in tier_files:
            tier_path.append(os.path.join(tier_folder, tier_file))
        tier_f = pd.read_excel(str(tier_path)[2:-2], header=None, index_col=None)

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
        self.lineEdit.setMaximumHeight(40)

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
                icon_y += 100
            else:
                icon_x += 70

        self.label = QLabel(scroll_content_2)
        self.label.setObjectName("Tier_Title")
        self.label.setText("\t티어   이름       승률")
        self.label.setStyleSheet("color: #9E9EAF;"
                                 "border-width: 0px;"
                                 "border-radius: 3px;")
        self.label.setGeometry(0, 0, 480, 40)

        self.tier_buttons = []
        self.tier_labels = []
        self.tier_tiers = [[] for i in range(6)]
        for j in range(tier_f[0].__len__()):
            # 티어 지수 계산(지금은 그냥 승률임)
            tier = tier_f[1][j] / 100.0
            if tier >= 0.55:
                tier = 0
            elif 0.52 <= tier < 0.55:
                tier = 1
            elif 0.50 <= tier < 0.52:
                tier = 2
            elif 0.48 <= tier < 0.50:
                tier = 3
            elif 0.45 <= tier < 0.48:
                tier = 4
            elif tier < 0.45:
                tier = 5
            self.tier_tiers[tier].append(j)

        for i in range(6):
            for j in range(self.tier_tiers[i].__len__() - 1):
                for k in range(self.tier_tiers[i].__len__() - 1):
                    if tier_f[1][j] > tier_f[1][j + 1]:
                        self.tier_tiers[i][j], self.tier_tiers[i][j + 1] = self.tier_tiers[i][j + 1], self.tier_tiers[i][j]

        for i in range(6):
            for j in self.tier_tiers[i]:
                button_2a = QPushButton(scroll_content_2)
                for k in range(icon_path.__len__()):
                    if (str(tier_f[0][j]) in icon_path[k]):
                        button_2a.setIcon(QIcon(icon_path[k]))
                button_2a.setIconSize(QtCore.QSize(45, 45))
                button_2a.setGeometry(tier_x, tier_y, 50, 50)
                button_2a.setObjectName(f"Tier_icon_{str(tier_f[0][j])}")
                button_2a.setText("")
                self.tier_buttons.append(button_2a)

                button_2b = QPushButton(scroll_content_2)
                button_2b.setIcon(QIcon(tier_icon_path[i]))
                button_2b.setIconSize(QtCore.QSize(45, 45))
                button_2b.setGeometry(tier_x + 50, tier_y, 50, 50)
                button_2b.setObjectName(f"Tier_tier_{str(tier_f[0][j])}")
                button_2b.setText("")
                self.tier_buttons.append(button_2b)

                # 버튼 라벨 추가
                label_2a = QLabel(scroll_content_2)
                label_2a.setText(str(tier_f[0][j]))
                label_2a.setObjectName(f"Tier_{str(tier_f[0][j])}")
                if (len(str(tier_f[0][j])) > 3):
                    label_2a.setText(str(tier_f[0][j][:3]) + "...")
                label_2a.setGeometry(tier_x + 100, tier_y, 70, 50)
                label_2a.setStyleSheet("color: #9E9EAF;")
                self.tier_labels.append(label_2a)

                label_2b = QLabel(scroll_content_2)
                label_2b.setText(str(tier_f[1][j]) + "%")
                label_2b.setObjectName(f"Tier_wr_{str(tier_f[0][j])}")
                label_2b.setGeometry(tier_x + 170, tier_y, 50, 50)
                label_2b.setStyleSheet("color: #9E9EAF;")
                self.tier_labels.append(label_2b)
                tier_x = 10
                tier_y += 55


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()
    sys.exit(app.exec_())