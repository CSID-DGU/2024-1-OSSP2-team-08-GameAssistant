import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

RecordWindowSource = uic.loadUiType("RecordFrame.ui")[0]
MatchScoreSource = uic.loadUiType("MatchRecord.ui")[0]

#region Class
class MatchJsonInfo():
    #Set Here
    isWinOrLose = False

    #Set Json Names
    result = "gameRank" #등수 혹은 승리여부
    matchTime = "playTime" #경기 시간
    playerKill = "playerKill" #플레이어의 킬수
    playerDeath = "PlayerDeaths" #플레이어의 데스 수
    playerAssistant = "playerAssistant" #플레이어의 어시스트 수
    playerDMG = "damageToPlayer" #플레이어가 준 데미지
    playerMMRBefore = "mmrBefore" #이전 MMR
    playerMMRAfter = "mmrAfter" #이후 MMR
    playerCharCode = "characterCode"

class PlayerJsonInfo():
    playerCharCode = "characterCode"
    playerName = "playerName"
    playerMMR = "playerMMR"
    playerWin = "playerWin"
    playerLose = "playerLose"

class RecordFrameUI(QWidget, RecordWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def SetPlayerInfo(self, jsonObj):
        playerCharCode = jsonObj[PlayerJsonInfo.playerCharCode]
        playerName = jsonObj[PlayerJsonInfo.playerName]
        playerMMR = jsonObj[PlayerJsonInfo.playerMMR]
        playerWin = jsonObj[PlayerJsonInfo.playerWin]
        playerLose = jsonObj[PlayerJsonInfo.playerLose]

        self.Nickname.setText(playerName)
        self.PlayerMMR.setText("MMR: "+str(playerMMR))
        self.Winlate.setText(str(round(playerWin/(playerWin+playerLose)*100,1))+"%")
        self.WinLose.setText(str(playerWin)+"승 "+str(playerLose)+"패")

        self.PlayerImg.setPixmap(QPixmap(("PlayerImg/"+str(playerCharCode)+".png")))
        return


    def AddMatchFrame(self, jsonObj):
        matchObj = MatchUI()
        matchObj.SetInfo(jsonObj)
        self.MatchesLayout.insertWidget(0, matchObj.MatchFrame)

class MatchUI(QWidget, MatchScoreSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        font = self.Result.font()
        font.setPointSize(12)
        self.Result.setFont(font)
        self.KDALate.setFont(font)
        self.MMR.setFont(font)
        self.DMG.setFont(font)

        font = self.KDA.font()
        font.setPointSize(14)
        font.setBold(True)
        self.KDA.setFont(font)




    def SetInfo(self, jsonObj):
        playerRank = jsonObj[MatchJsonInfo.result]
        matchTime = jsonObj[MatchJsonInfo.matchTime]
        playerKill = jsonObj[MatchJsonInfo.playerKill]
        playerDeath = jsonObj[MatchJsonInfo.playerDeath]
        playerAssistant = jsonObj[MatchJsonInfo.playerAssistant]
        playerDMG = jsonObj[MatchJsonInfo.playerDMG]
        playerMMRBefore = jsonObj[MatchJsonInfo.playerMMRBefore]
        playerMMRAfter = jsonObj[MatchJsonInfo.playerMMRAfter]
        playerMMRGain = playerMMRAfter - playerMMRBefore
        playerCharCode = jsonObj[MatchJsonInfo.playerCharCode]

        if not MatchJsonInfo.isWinOrLose:
            if playerRank == 1:
                self.Result.setStyleSheet("color: blue")
                self.Result.setText("승리")               
                self.MatchFrame.setStyleSheet("background-color: rgb(236, 242, 255)")
            elif playerRank == 2:
                self.Result.setStyleSheet("color: red")
                self.Result.setText("패배")          
                self.MatchFrame.setStyleSheet("background-color: rgb(255, 241, 243)")
        else:
            self.Result.setText(playerRank,"위")
            if playerRank == 1:
                self.Result.setStyleSheet("Color: green")
            elif playerRank == 2:
                self.Result.setStyleSheet("Color: blue")
            else:
                self.Result.setStyleSheet("Color: gray")
        
        
        self.MatchTime.setText(str(matchTime//60)+"분 "+str(matchTime%60)+"초")
        self.KDA.setText(str(playerKill)+"/"+"<span style='color: red;'>"+str(playerDeath)+"</span>"+"/"+str(playerAssistant))
        self.KDALate.setText("KDA: "+"Perfact" if playerDeath == 0 else str(round((playerKill+playerAssistant)/playerDeath,1)))
        self.DMG.setText("DMG: "+str(playerDMG))

        if playerMMRGain > 0:
            self.MMR.setText("MMR: "+str(playerMMRAfter)+"<span style='color: blue;'> ▲"+str(playerMMRGain)+"</span>")
        else:
            self.MMR.setText("MMR: "+str(playerMMRAfter)+"<span style='color: red;'> ▼"+str(-playerMMRGain)+"</span>")
        
        
        self.CharIMG.setPixmap(QPixmap(("CharImg/"+str(playerCharCode)+".png")))
#region Class End

#region function
def API_GetPlayerInfo(playerID):
    file = open("test/PlayerJson.json", 'r', encoding='utf-8') #for Debug
    playerJsonObj = json.load(file)
    return playerJsonObj

def API_GetPlayerMatchInfo(playerID, num):
    file = open("test/MatchJson"+str(num)+".json", 'r', encoding='utf-8')#for Debug
    matchJsonObj = json.load(file)
    return matchJsonObj

#region function end

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    recordFrameObj = RecordFrameUI()
    recordFrameObj.show()

    recordFrameObj.SetPlayerInfo(API_GetPlayerInfo("abc"))

    #for Debug
    recordFrameObj.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))
    recordFrameObj.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))

    app.exec_()