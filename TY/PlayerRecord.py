import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

RecordWindowSource = uic.loadUiType("window.ui")[0]
MatchScoreSource = uic.loadUiType("MatchRecord.ui")[0]


class RecordWindow(QMainWindow, RecordWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MatchUI(QWidget, MatchScoreSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MatchjsonInfo():
    kill = "PlayerKill"

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = RecordWindow() 
    matchUI = MatchUI()
    myWindow.show()

    app.exec_()

def AddMatch(MatchJson):
    matchUI = MatchUI().ScoreWidget
    jsonObj = json.loads(MatchJson)


    myWindow.MatchLayout.addWidget(matchUI)