import sys, os
import json
import api
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
#from mmrUItest import mmrUI

mmrUisrc = uic.loadUiType("../Data/UI/MMRUI/mmrUI.ui")[0]
MMRUIWindowSource = uic.loadUiType("../Data/UI/MMRUI/MMRUI3P.ui")[0]

class PlayerMMRInfo():
    playerCharCode = "characterCode"
    playerName = "nickname"
    playerMMR = "mmr"
    playerRank = 'rank'
    playerGames = "totalGames"
    playerWin = "totalWins"
    playerAvgRank = 'averageRank'
    playerAvgKill= 'averageKills'
    playerAvgAssist = 'averageAssistants'

    charUsage = 'usages'
    charTop3 = 'top3'
    charGameRank = 'averageRank'
    

class MMRWindowUI(QMainWindow, MMRUIWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def UpdateData(self , nickname_list):
        for nickname in nickname_list:
            playerMMRData = API_GetPlayerMMRInfo(nickname)

            if playerMMRData == None:
                #404
                return
            self.AddMMRFrame(playerMMRData)
        

    def AddMMRFrame(self, jsonObj):
        mmrFrame = mmrUI()
        mmrFrame.SetInfo(jsonObj)
        self.MMRLayout.addWidget(mmrFrame)

class mmrUI(QWidget, mmrUisrc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def SetInfo(self, jsonObj):
        # 첫 번째 유저의 데이터 가져오기
        Charactercode = jsonObj[PlayerMMRInfo.playerCharCode]
        Nickname = jsonObj[PlayerMMRInfo.playerName]
        rankPoint = jsonObj[PlayerMMRInfo.playerMMR]
        rankNum = jsonObj[PlayerMMRInfo.playerRank]
        userTotal = jsonObj[PlayerMMRInfo.playerGames]
        userWin = jsonObj[PlayerMMRInfo.playerWin]
        useravgRank = jsonObj[PlayerMMRInfo.playerAvgRank]
        useravgKill = jsonObj[PlayerMMRInfo.playerAvgKill]
        useravgAssistant = jsonObj[PlayerMMRInfo.playerAvgAssist]
        
        # 첫 번째 캐릭터의 데이터 가져오기
        charUsage = jsonObj[PlayerMMRInfo.charUsage]
        charTop3 = jsonObj[PlayerMMRInfo.charTop3]
        chargameRank = jsonObj[PlayerMMRInfo.charGameRank]
        
        self.charimage.setPixmap(QPixmap("imagefile/" + str(Charactercode) + ".png").scaled(241, 201, Qt.KeepAspectRatio))
        self.nickname.setText(Nickname)
        self.rankpoint.setText("점수: " + str(rankPoint))
        self.ranknum.setText("순위: " + str(rankNum))
        self.tierimage.setPixmap(QPixmap("imagefile/Eternity.png").scaled(81, 91, Qt.KeepAspectRatio))
        self.Userstat.setText("User stat")
        self.Gamestat.setText(str(userTotal) + "전 " + str(userWin) + "승 " + str(round(userWin/(userTotal)*100,2))+"%")
        self.avgRank.setText("평균 순위: " + str(useravgRank))
        self.avgKill.setText("평균 킬: " + str(useravgKill))
        self.avgAssistant.setText("평균 어시: " + str(useravgAssistant))
        self.Charstat.setText("Charcter stat")
        self.charusage.setText("플레이 횟수: " + str(charUsage))
        self.charIntop3.setText("In top3: " + str(charTop3))
        self.charavgRank.setText("평균 순위: " + str(chargameRank))
#region Class End

#region function
def API_GetPlayerMMRInfo(playerID):
    factory = api.APIFactory()
    seasonId = factory.get_current_seasonId()
    if seasonId == None:
        return PlayerJsonInfo.default
        
    data=factory.get_user_data(nickname=playerID, seasonId=seasonId)
    if data == None:
        return None
    else:
        stats = [stats for stats in data['userStats'] if stats['matchingMode'] == 3]
        mmr=[]
        rank=[]
        games=[]
        win=[]
        avg_rank=[]
        avg_kill=[]
        avg_assist=[]
        for stat in stats:
            mmr.append(stat['mmr'])
            rank.append(stat['rank'])
            games.append(stat['totalGames'])
            win.append(stat['totalWins'])
            avg_rank.append(stat['averageRank'])
            avg_kill.append(stat['averageKills'])
            avg_assist.append(stat['averageAssistants'])

        #평균 계산
        mmr = round(sum(mmr)/len(mmr))
        rank = round(sum(rank)/len(rank))
        games = sum(games)
        win = sum(win)
        avg_rank=round(sum(avg_rank)/len(avg_rank))
        avg_rank=round(sum(avg_kill)/len(avg_kill))
        avg_assist=round(sum(avg_assist)/len(avg_assist))
        

        
                          #솔로에서 가장 많이 쓴 캐릭터
        playerJsonObj = {PlayerMMRInfo.playerCharCode : data['userStats'][0]['characterStats'][0]['characterCode'], \
                         PlayerMMRInfo.playerName : data['userStats'][0]['nickname'], \
                         PlayerMMRInfo.playerMMR : mmr, \
                         PlayerMMRInfo.playerRank : rank, \
                         PlayerMMRInfo.playerGames : games, \
                         PlayerMMRInfo.playerWin : win, \
                         PlayerMMRInfo.playerAvgRank : avg_rank, \
                         PlayerMMRInfo.playerAvgKill : avg_kill, \
                         PlayerMMRInfo.playerAvgAssist : avg_assist, \
                         PlayerMMRInfo.charUsage : data['userStats'][0]['characterStats'][0]['usages'], \
                         PlayerMMRInfo.charTop3 : data['userStats'][0]['characterStats'][0]['top3'], \
                         PlayerMMRInfo.charGameRank : data['userStats'][0]['characterStats'][0]['averageRank']}
        return playerJsonObj

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    window.UpdateData(['한동그라미', '삼다수는맛있어', '커리'])
    window.showMinimized()
    window.showNormal()
    sys.exit(app.exec_())
