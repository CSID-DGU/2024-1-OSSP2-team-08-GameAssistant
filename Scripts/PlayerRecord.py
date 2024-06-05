import sys, os
import json
import api
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QCursor


RecordWindowSource = uic.loadUiType("Data/UI/Record/RecordFrame.ui")[0]
MatchScoreSource = uic.loadUiType("Data/UI/Record/MatchRecord.ui")[0]

#region Class
class MatchJsonInfo():
    #Set Here
    isWinOrLose = False

    #Set Json Names
    result = "gameRank" #등수 혹은 승리여부
    matchTime = "playTime" #경기 시간
    playerKill = "playerKill" #플레이어의 킬수
    playerDeath = "playerDeaths" #플레이어의 데스 수
    playerAssistant = "playerAssistant" #플레이어의 어시스트 수
    playerDMG = "damageToPlayer" #플레이어가 준 데미지
    playerMMRBefore = "mmrBefore" #이전 MMR
    playerMMRAfter = "mmrAfter" #이후 MMR
    playerCharCode = "characterNum"

    default = {result : 0, matchTime : 0, playerKill : 0, playerDeath : -1, playerAssistant : 0,\
               playerDMG : 0, playerMMRBefore : 0, playerMMRAfter : 0, playerCharCode : 0}

class PlayerJsonInfo():
    playerCharCode = "characterCode"
    playerName = "nickname"
    playerMMR = "mmr"
    playerWin = "totalWins"
    playerLose = "playerLose"
    playerGames = "totalGames"

    default = {playerCharCode : 0, playerName : "", playerMMR : 0, \
               playerWin : 0, playerLose : 0, playerGames : -1}

class RecordFrameUI(QWidget, RecordWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.MatchesLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollAreaWidgetContents_2.setLayout(self.MatchesLayout)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.MatchesLayout.addItem(self.spacer)

        self.NameSearch.clicked.connect(self.UpdateData)
        self.NameInput.returnPressed.connect(self.UpdateData)
        self.NameSearch.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.PlayerInfoFrame.hide()

    def SetPlayerInfo(self, jsonObj):
        playerCharCode = jsonObj[PlayerJsonInfo.playerCharCode]
        playerName = jsonObj[PlayerJsonInfo.playerName]
        playerMMR = jsonObj[PlayerJsonInfo.playerMMR]
        playerWin = jsonObj[PlayerJsonInfo.playerWin]
        playerGames = jsonObj[PlayerJsonInfo.playerGames]

        self.Nickname.setText(playerName)
        self.PlayerMMR.setText("MMR: "+str(playerMMR))
        self.Winlate.setText(str(round(playerWin/(playerGames)*100,1))+"%")
        self.WinLose.setText(str(playerWin)+"승 "+str(playerGames - playerWin)+"패")

        self.PlayerImg.setPixmap(QPixmap(("PlayerImg/"+str(playerCharCode)+".png")))
        return

    def AddMatchFrame(self, jsonObj):
        matchObj = MatchUI()
        matchObj.SetInfo(jsonObj)
        self.MatchesLayout.insertWidget(0, matchObj.MatchFrame)

    def UpdateData(self):
            usernameSrc = self.NameInput.text()
            playerData = API_GetPlayerInfo(usernameSrc)
            if playerData == None:
                #404
                return

            #for Debug
            self.PlayerInfoFrame.show()
            self.Nickname.setText(usernameSrc)
            self.PlayerMMR.setText("MMR: " + str(playerData["mmr"]))
            self.WinLose.setText("플레이 게임: "+str(playerData["totalGames"]))
            self.Winlate.setText("승률: {:.2f}%".format(float(playerData["totalWins"]) / playerData["totalGames"] * 100))
            #self.SetPlayerInfo(playerData)

            match_data = API_GetPlayerMatchInfo(usernameSrc)
            if match_data == None:
                #404
                return
            for i in range(1, 20 if len(match_data) > 20 else len(match_data)):
                self.AddMatchFrame(match_data[i])

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
        print(jsonObj)
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
            else:
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
    factory = api.APIFactory()
    seasonId = factory.get_current_seasonId()
    if seasonId == None:
        return PlayerJsonInfo.default
        
    data=factory.get_user_data(nickname=playerID, seasonId=seasonId)
    if data == None:
        return None
    else:
        data = data['userStats'][0] #matchingTeamMode에 따라 갈림
        
        playerJsonObj = {PlayerJsonInfo.playerCharCode : data['characterStats'][0]['characterCode'], \
                         PlayerJsonInfo.playerName : data['nickname'], \
                         PlayerJsonInfo.playerMMR : data['mmr'], \
                         PlayerJsonInfo.playerWin : data['totalWins'], \
                         PlayerJsonInfo.playerLose : data['totalGames'] - data['totalWins'], \
                         PlayerJsonInfo.playerGames : data['totalGames']}
    return playerJsonObj

def API_GetPlayerMatchInfo(playerID):
    factory=api.APIFactory()
    data = factory.get_match_data(playerID)
    match_info_list = []
    if data == None:
        return MatchJsonInfo.default
    else:
        for match in data['userGames']:
            if match['matchingMode'] == 3: #랭크 게임만
                matchJsonObj = {MatchJsonInfo.result : match['gameRank'],\
                                MatchJsonInfo.matchTime : match['playTime'],\
                                MatchJsonInfo.playerKill : match['playerKill'],\
                                MatchJsonInfo.playerDeath : match['playerDeaths'],\
                                MatchJsonInfo.playerAssistant : match['playerAssistant'],\
                                MatchJsonInfo.playerDMG : match['damageToPlayer'],\
                                MatchJsonInfo.playerMMRBefore : match['mmrBefore'],\
                                MatchJsonInfo.playerMMRAfter : match['mmrAfter'],\
                                MatchJsonInfo.playerCharCode : match['characterNum']}
                match_info_list.append(matchJsonObj)
    return match_info_list

#region function end
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    
    recordFrameObj = RecordFrameUI()
    recordFrameObj.show()
    
    app.exec_()
