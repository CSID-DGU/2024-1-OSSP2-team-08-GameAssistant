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
    #Edit Here
    isWinOrLose = False

    #Json Names
    playerRank = "gameRank" #등수 혹은 승리여부
    matchTime = "playTime" #경기 시간
    playerKill = "playerKill" #플레이어의 킬수
    playerDeath = "PlayerDeaths" #플레이어의 데스 수
    playerAssistant = "playerAssistant" #플레이어의 어시스트 수
    playerDMG = "damageToPlayer" #플레이어가 준 데미지
    playerMMRBefore = "mmrBefore" #이전 MMR
    playerMMRAfter = "mmrAfter" #이후 MMR
    playerCharCode = "characterCode"

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = RecordWindow() 
    matchUI = MatchUI()
    myWindow.show()

    app.exec_()

def AddMatch(MatchJson):
    matchUI = MatchUI().ScoreWidget
    jsonObj = json.loads(MatchJson)

    playerRank = jsonObj[MatchjsonInfo.playerRank]
    matchTime = jsonObj[MatchjsonInfo.matchTime]
    playerKill = jsonObj[MatchjsonInfo.playerKill]
    playerDeath = jsonObj[MatchjsonInfo.playerDeath]
    playerAssistant = jsonObj[MatchjsonInfo.playerAssistant]
    playerDMG = jsonObj[MatchjsonInfo.playerDMG]
    playerMMRBefore = jsonObj[MatchjsonInfo.playerMMRBefore]
    playerMMRAfter = jsonObj[MatchjsonInfo.playerMMRAfter]
    playerMMRGain = playerMMRAfter - playerMMRBefore
    playerCharCode = jsonObj[MatchjsonInfo.playerCharCode]

    if not MatchjsonInfo.isWinOrLose:
        if playerRank == 1:
            matchUI.playerRank = "승리"
            matchUI.playerRank = color
        elif playerRank == 2:
            matchUI.playerRank = "패배"
            matchUI.playerRank = color
    else:
        if playerRank == 1:
            matchUI.playerRank = "승리"
            matchUI.playerRank = color
        elif playerRank == 2:
            matchUI.playerRank = "패배"
            matchUI.playerRank = color
    
    
    matchUI.matchTime = (matchTime//60,"분 ",matchTime%60"초")
    matchUI.playerKDA = playerKill,"/",playerDeath,"/",playerAssistant
    matchUI.playerKDA2 = "KDA: ","Perfact" if playerDeath == 0 else (playerKill+playerAssistant)/playerDeath,"%"
    matchUI.playerDMG = "DMG: ",playerDMG
    matchUI.playerMMR = "MMR: ",playerMMRAfter,"^",playerMMRGain
    
    matchUI.playerImg = playerCharCode

    myWindow.MatchLayout.addWidget(matchUI)