import sys, os
import json
from API import api
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
#from mmrUItest import mmrUI

mmrUisrc = uic.loadUiType("Data/UI/MMRUI/mmrUI.ui")[0]
MMRUIWindowSource = uic.loadUiType("Data/UI/MMRUI/MMRUI3P.ui")[0]
MMRJsonPath = "Data/TestJson/playersMMR/Player"

class PlayerMMRInfo():
    playerCharCode = "characterCode"
    playerName = "nickname"
    playerMMR = "mmr"
    userRank = "userRank"
    
    playerWin = "totalWins"
    playerGames = "totalGames"
    playerAvgRank = 'averageRank'
    playerAvgKill= 'averageKills'
    playerTK = 'totalTeamKills'

    charGames = 'charTotalGames'
    charWin = 'charWins'
    charAvgRank = 'charAverageRank'

class MMRWindowUI(QMainWindow, MMRUIWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def UpdateData(self , nickname_list):
        for region in nickname_list:
            nickname = region['nickname']
            playerMMRData = API_GetPlayerMMRInfo(nickname)
            if playerMMRData == None:
                #404
                return
            self.AddMMRFrame(playerMMRData)
                   
        

    def AddMMRFrame(self, jsonObj):
        mmrFrame = mmrUI()
        mmrFrame.SetInfo(jsonObj)
        self.MMRLayout.addWidget(mmrFrame.mmrItemFrame)

class mmrUI(QWidget, mmrUisrc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def SetInfo(self, jsonObj):
        # 첫 번째 유저의 데이터 가져오기
        Charactercode = jsonObj[PlayerMMRInfo.playerCharCode]
        Nickname = jsonObj[PlayerMMRInfo.playerName]
        rankPoint = jsonObj[PlayerMMRInfo.playerMMR]
        userRank = jsonObj[PlayerMMRInfo.userRank]

        userTotal = jsonObj[PlayerMMRInfo.playerGames]
        userWin = jsonObj[PlayerMMRInfo.playerWin]
        userWinLate = round(userWin/userTotal * 100, 2)
        useravgRank = jsonObj[PlayerMMRInfo.playerAvgRank]
        useravgKill = jsonObj[PlayerMMRInfo.playerAvgKill]
        userTK = jsonObj[PlayerMMRInfo.playerTK]
        userAvgTK = round(userTK/userTotal, 2)
        
        # 첫 번째 캐릭터의 데이터 가져오기
        charGames = jsonObj[PlayerMMRInfo.charGames]
        charWin = jsonObj[PlayerMMRInfo.charWin]
        charWinLate = round(charWin/charGames*100, 2)
        charAvgRank = jsonObj[PlayerMMRInfo.charAvgRank]
        
        self.charimage.setPixmap(QPixmap(":/champions/Champions/Mini/"+str(Charactercode)+".png").scaled(self.charimage.size(), Qt.KeepAspectRatio))
        playerTier = ""
        if userRank <= 200:
            playerTier = "Eternity"
        elif userRank <= 700:
            playerTier = "Demigod"
        elif rankPoint >= 6800:
            playerTier = "Mithril"
        elif rankPoint >= 5200:
            playerTier = "Diamond"
        elif rankPoint >= 3800:
            playerTier = "Platinum"
        elif rankPoint >= 2600:
            playerTier = "Gold"
        elif rankPoint >= 1600:
            playerTier = "Silver"
        elif rankPoint >= 800:
            playerTier = "Bronze"
        else:
            playerTier = "Iron"

        self.tierimage.setPixmap(QPixmap(":/tiers/Tier/"+playerTier+".png").scaled(self.tierimage.size(), Qt.KeepAspectRatio))
        self.nickname.setText(Nickname)
        self.winLate.setText("  승률: " + str(userWinLate) + "%")
        self.mmr.setText("  MMR: " + str(rankPoint))

        self.totalGame.setText("게임 수: "+ str(userTotal))
        self.avgRank.setText("평균 순위: "+str(useravgRank))
        self.avgKill.setText("평균 Kill: "+str(useravgKill))
        self.avgTK.setText("평균 TK: "+str(userAvgTK))

        self.charGame.setText("플레이 횟수: " + str(charGames))
        self.charWinlate.setText("승률: " + str(charWinLate) + "%")
        self.charAvgRank.setText("평균 순위: " + str(charAvgRank))
#region Class End

#region function
def API_GetPlayerMMRInfo(playerID):
    factory = api.APIFactory()
    seasonId = factory.get_current_seasonId()
    if seasonId == None:
        return PlayerMMRInfo.default
        
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
        userRank=[]
        tk= 0
        for stat in stats:
            mmr.append(stat['mmr'])
            rank.append(stat['rank'])
            games.append(stat['totalGames'])
            win.append(stat['totalWins'])
            avg_rank.append(stat['averageRank'])
            avg_kill.append(stat['averageKills'])
            tk = stat['totalTeamKills']
            userRank = stat['rank']

        #평균 계산
        mmr = round(sum(mmr)/len(mmr))
        rank = round(sum(rank)/len(rank))
        games = sum(games)
        win = sum(win)
        avg_kill = round(sum(avg_kill)/len(avg_kill), 2)
        avg_rank=round(sum(avg_rank)/len(avg_rank), 2)
        

        
                          #솔로에서 가장 많이 쓴 캐릭터
        playerJsonObj = {PlayerMMRInfo.playerCharCode : data['userStats'][0]['characterStats'][0]['characterCode'], \
                         PlayerMMRInfo.playerName : data['userStats'][0]['nickname'], \
                         PlayerMMRInfo.playerMMR : mmr, \
                         PlayerMMRInfo.userRank: userRank, \
                         PlayerMMRInfo.playerGames : games, \
                         PlayerMMRInfo.playerWin : win, \
                         PlayerMMRInfo.playerAvgRank : avg_rank, \
                         PlayerMMRInfo.playerAvgKill : avg_kill, \
                         PlayerMMRInfo.playerTK : tk, \
                         PlayerMMRInfo.charGames : data['userStats'][0]['characterStats'][0]['usages'], \
                         PlayerMMRInfo.charWin : data['userStats'][0]['characterStats'][0]['wins'], \
                         PlayerMMRInfo.charAvgRank : data['userStats'][0]['characterStats'][0]['averageRank']}

        return playerJsonObj

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    #window.UpdateData(['한동그라미', '삼다수는맛있어', '커리'])
    #window.showMinimized()
    #window.showNormal()
    sys.exit(app.exec_())