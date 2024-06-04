import sys
import json
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

TierWindowSource = uic.loadUiType("Data/UI/TierUI/TierWindow.ui")[0]
TierItemSource = uic.loadUiType("Data/UI/TierUI/TierItem.ui")[0]

class TierWindowUI(QWidget, TierWindowSource):
    def __init__(self):
        super().__init__()

        self.sortIndex = -1
        self.sortIsReverse = True

        self.setupUi(self)
        self.TierLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.TierLayout.setSpacing(0)
        self.TierLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaWidgetContents_2.setLayout(self.TierLayout)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)   

        file = open('./Data/TestJson/championTier/champion.json', 'r', encoding='utf-8') #For Debug

        c_file = json.load(file)
        self.c_lists = [[] for i in range(c_file["data"].__len__())]
        i = 0
        tier = 0
        for data in c_file["data"]:
            self.c_lists[i].append(c_file["data"][data]["name"])
            self.c_lists[i].append(c_file["data"][data]["Winrate"])
            self.c_lists[i].append(c_file["data"][data]["Pickrate"])
            self.c_lists[i].append(c_file["data"][data]["Top3"])
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
            self.c_lists[i].append(TierItemUI(self.c_lists[i]))
            print(self.c_lists)
            i += 1

        self.Attribute01btn.clicked.connect(lambda:self.sortTiers(1))
        self.Attribute02btn.clicked.connect(lambda:self.sortTiers(2))
        self.Attribute03btn.clicked.connect(lambda:self.sortTiers(3))
        self.Attribute01btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Attribute02btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Attribute03btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        

        self.TierLayout.addItem(self.spacer)
        self.sortTiers(1)

    def sortTiers(self, num):
        self.c_lists.sort(key = lambda x: x[num])
        if self.sortIndex != num:
            self.sortIsReverse = True
            self.c_lists.reverse()
            self.sortIndex = num
        else:
            if self.sortIsReverse:
                self.sortIsReverse = False
            else:
                self.sortIsReverse = True
                self.c_lists.reverse()
        
        if self.sortIndex == 1:
            self.Attribute01btn.setChecked(True)
            self.Attribute02btn.setChecked(False)
            self.Attribute03btn.setChecked(False)
        elif self.sortIndex == 2:
            self.Attribute01btn.setChecked(False)
            self.Attribute02btn.setChecked(True)
            self.Attribute03btn.setChecked(False)
        elif self.sortIndex == 3:
            self.Attribute01btn.setChecked(False)
            self.Attribute02btn.setChecked(False)
            self.Attribute03btn.setChecked(True)
        

        for i in range(self.c_lists.__len__()):
            self.TierLayout.insertWidget(i, self.c_lists[i][-1].MatchFrame)

        

class TierItemUI(QWidget, TierItemSource):
    def __init__(self, c_list):
        super().__init__()
        self.setupUi(self)

        font = self.CharName.font()
        font.setPointSize(12)
        self.Attribute01.setFont(font) #pick
        self.Attribute02.setFont(font) #win
        self.Attribute03.setFont(font) #top3
        self.Attribute01.setAlignment(QtCore.Qt.AlignCenter)
        self.Attribute02.setAlignment(QtCore.Qt.AlignCenter)
        self.Attribute03.setAlignment(QtCore.Qt.AlignCenter)
        if c_list != None :
            self.SetInfo(c_list)

    def SetInfo(self, c_list):
        #Add Img Change Here

        self.CharName.setText("<span style = 'font-size:12px; text-align: center;'>" + c_list[0] + "</span>")
        self.Attribute01.setText("<span style = 'font-size:12px; text-align: right;'>" + str(c_list[1]) + "</span>")
        self.Attribute02.setText("<span style = 'font-size:12px; text-align: center;'>" + str(c_list[2]) + "</span>")  
        self.Attribute03.setText("<span style = 'font-size:12px; text-align: center;'>" + str(c_list[3]) + "</span>")  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TierWindowUI()
    window.show()
    sys.exit(app.exec_())