import sys
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic
import champIcons_rc

TierWindow = uic.loadUiType("TierList.ui")[0]
TierFrame = uic.loadUiType("TierFrame.ui")[0]
IconFrame = uic.loadUiType("IconFrame.ui")[0]

class TierWindowUI(QMainWindow, TierWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialized = False
        self.lineEdit.textChanged.connect(self.filterButtons)
        self.TierSort.clicked.connect(lambda: self.sortTiers('tier'))
        self.NameSort.clicked.connect(lambda: self.sortTiers('name'))
        self.WinrateSort.clicked.connect(lambda: self.sortTiers('winrate'))
        self.PickRateSort.clicked.connect(lambda: self.sortTiers('pickrate'))
        self.BanRateSort.clicked.connect(lambda: self.sortTiers('banrate'))

    def initialize(self):
        if not self.initialized:
            for i in range(1, len(os.listdir("./c_icons/ChampionIcon"))):
                if i >= len(GetCharacterJson()["data"]) + 1:
                    break
                self.AddIconFrame(i)
            for i in range(1, len(GetCharacterJson()["data"]) + 1):
                self.AddTierFrame(i)
            self.initialized = True

    def AddTierFrame(self, num):
        frame1 = TierFrameUI()
        frame1.SetTierFrame(num, GetCharacterJson())
        self.ChampInfoLayout.addWidget(frame1)

    def AddIconFrame(self, num):
        row = (num - 1) // 4
        col = (num - 1) % 4
        frame2 = IconFrameUI()
        frame2.SetIconFrame(num, GetCharacterJson())
        self.ChampIconLayout.addWidget(frame2, row, col)

    def filterButtons(self, text):
        text = text.replace(" ", "")
        for i in range(self.ChampIconLayout.count()):
            item = self.ChampIconLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    if text.lower() in widget.champLabel.text().replace(" ", "").lower():
                        widget.setVisible(True)
                    else:
                        widget.setVisible(False)

    def sortTiers(self, criteria):
        frames = []
        for i in range(self.ChampInfoLayout.count()):
            item = self.ChampInfoLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    frames.append(widget)

        if criteria == 'tier':
            frames.sort(key=lambda x: x.tier)
        elif criteria == 'name':
            frames.sort(key=lambda x: x.name.lower())
        elif criteria == 'winrate':
            frames.sort(key=lambda x: x.winrate, reverse=True)
        elif criteria == 'pickrate':
            frames.sort(key=lambda x: x.pickrate, reverse=True)
        elif criteria == 'banrate':
            frames.sort(key=lambda x: x.banrate, reverse=True)

        # 기존 위젯 제거
        while self.ChampInfoLayout.count():
            item = self.ChampInfoLayout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # 정렬된 위젯 다시 추가
        for frame in frames:
            self.ChampInfoLayout.addWidget(frame)

class TierFrameUI(QWidget, TierFrame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def SetTierFrame(self, num, json):
        self.name = json["data"][str(num)]["name"]
        self.winrate = json["data"][str(num)]["Winrate"]
        self.pickrate = json["data"][str(num)]["Pickrate"]
        self.banrate = json["data"][str(num)]["Banrate"]
        if self.winrate >= 55.0:
            self.tier = 0
        elif 55.0 > self.winrate >= 52.0:
            self.tier = 1
        elif 52.0 > self.winrate >= 50.0:
            self.tier = 2
        elif 50.0 > self.winrate >= 48.0:
            self.tier = 3
        elif 48.0 > self.winrate >= 45.0:
            self.tier = 4
        elif 45.0 > self.winrate:
            self.tier = 5
        self.CIcon.setPixmap(QPixmap(":/champions/ChampionIcon/" + str(num) + ".png"))
        self.TIcon.setPixmap(QPixmap(":/tiers/TierIcons/0" + str(self.tier) + ".png"))
        self.Name.setText(f'{self.name}')
        self.Winrate.setText(f'{self.winrate}%')
        self.Pickrate.setText(f'{self.pickrate}%')
        self.Banrate.setText(f'{self.banrate}%')

class IconFrameUI(QWidget, IconFrame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def SetIconFrame(self, num, json):
        name = json["data"][str(num)]["name"]
        self.champIcon.setPixmap(QPixmap(":/champions/ChampionIcon/" + str(num) + ".png"))
        self.champLabel.setText(f'{name}')

def GetCharacterJson():
    file = open("champion/champion.json", 'r', encoding='utf-8')
    return json.load(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TierWindowUI()
    window.initialize()
    window.show()
    sys.exit(app.exec_())