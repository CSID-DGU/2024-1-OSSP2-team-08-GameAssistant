import sys, os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

current_dir = os.path.dirname(__file__)
ui_file_path1 = os.path.join(current_dir, '..', 'Data', 'UI', 'Record', 'RecordFrame.ui')
ui_file_path1 = os.path.abspath(ui_file_path1)
ui_file_path2 = os.path.join(current_dir, '..', 'Data', 'UI', 'Record', 'MatchRecord.ui')
ui_file_path2 = os.path.abspath(ui_file_path2)
json_file_path1 = os.path.join(current_dir, '..', 'Data', 'TestJson', 'playerJson', 'PlayerJson.json')
json_file_path1 = os.path.abspath(json_file_path1)
json_file_path2 = os.path.join(current_dir, '..', 'Data', 'TestJson', 'playerJson')
json_file_path2 = os.path.abspath(json_file_path2)
RecordWindowSource = uic.loadUiType(ui_file_path1)[0]
MatchScoreSource = uic.loadUiType(ui_file_path2)[0]

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
        self.MatchesLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollAreaWidgetContents_2.setLayout(self.MatchesLayout)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.MatchesLayout.addItem(self.spacer)



        self.UpdateData()

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

    def UpdateData(self):
            self.SetPlayerInfo(API_GetPlayerInfo("abc"))

            #for Debug
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",2))
            self.AddMatchFrame(API_GetPlayerMatchInfo("abc",1))




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
                #self.Result.setStyleSheet("color: blue")
                self.Result.setText("<span style='color: blue; font-size:15px;'>승리")               
                #self.MatchFrame.setStyleSheet("background-color: rgb(236, 242, 255)")
            elif playerRank == 2:
                #self.Result.setStyleSheet("color: red")
                self.Result.setText("<span style='color: red; font-size:15px;'>패배")          
                #self.MatchFrame.setStyleSheet("background-color: rgb(255, 241, 243)")
        else:
            self.Result.setText(playerRank,"위")
            if playerRank == 1:
                self.Result.setStyleSheet("Color: green")
            elif playerRank == 2:
                self.Result.setStyleSheet("Color: blue")
            else:
                self.Result.setStyleSheet("Color: gray")
        
        
        self.MatchTime.setText(str(matchTime//60)+"분 "+str(matchTime%60)+"초")
        self.KDA.setText("<span style='font-size:19px;'>"+str(playerKill)+" / "+"<span style='color: red;'>"+str(playerDeath)+"</span>"+" / "+str(playerAssistant)+"</span>")
        self.KDALate.setText("<span style='font-size:15px;'>"+"KDA: "+ ("Perfact" if playerDeath == 0 else str(round((playerKill+playerAssistant)/playerDeath,1)))+"</span>")
        self.DMG.setText("<span style='font-size:15px;'>"+"DMG: "+str(playerDMG)+"</span>")

        if playerMMRGain > 0:
            self.MMR.setText("<span style='font-size:15px;'>"+"MMR: "+str(playerMMRAfter)+"<span style='color: blue;'> ▲"+str(playerMMRGain)+"</span>"+"</span>")
        else:
            self.MMR.setText("<span style='font-size:15px;'>"+"MMR: "+str(playerMMRAfter)+"<span style='color: red;'> ▼"+str(-playerMMRGain)+"</span>"+"</span>")
        
        
        self.CharIMG.setPixmap(QPixmap(("CharImg/"+str(playerCharCode)+".png")))
#region Class End

#region function
def API_GetPlayerInfo(playerID):
    file = open(json_file_path1, 'r', encoding='utf-8') #for Debug, Fix Later
    playerJsonObj = json.load(file)
    return playerJsonObj

def API_GetPlayerMatchInfo(playerID, num):
    file = open(json_file_path2+"\\MatchJson"+str(num)+".json", 'r', encoding='utf-8')#for Debug, Fix Later
    matchJsonObj = json.load(file)
    return matchJsonObj

#region function end

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    
    recordFrameObj = RecordFrameUI()
    recordFrameObj.show()

    app.exec_()