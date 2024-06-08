import sys, os
import json
from API.api import APIFactory, APICallRunnable
import pyautogui
from PyQt5.QtCore import Qt,QThreadPool
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
#from mmrUItest import mmrUI

mmrUisrc = uic.loadUiType("Data/UI/MMRUI/mmrUI.ui")[0]
MMRUIWindowSource = uic.loadUiType("Data/UI/MMRUI/MMRWindow.ui")[0]
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
        self.thread_pool = QThreadPool()
        self.playerIdx = 0
        self.nickname_list = None

        self.IntroFrame.show()
        self.SearchFrame.hide()
        self.ErrorFrame.hide()
        self.SearchFrame_2.hide()


    def UpdateData(self , nickname_list):
        print("UpdateData Called")
        if self.playerIdx > 2:
            self.playerIdx = 0
            self.nickname_list = None
            self.SearchFrame_2.hide()
            return
        elif self.playerIdx == 0:
            self.IntroFrame.hide()
            self.SearchFrame.show()
            while self.MMRLayout.count() > 0:
                item = self.MMRLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.nickname_list = nickname_list
            self.SearchName.setText(nickname_list[0]['nickname'] + "\n" + nickname_list[1]['nickname'] + "\n" + nickname_list[2]['nickname'])
            self.SearchName.setAlignment(Qt.AlignCenter)
        else:
            self.SearchFrame.hide()
            self.SearchFrame_2.show()
        nickname = nickname_list[self.playerIdx]['nickname']
        self.API_GetPlayerMMRInfo(nickname)
            
                   
    def AddMMRFrame(self, jsonObj):
        mmrFrame = mmrUI()
        mmrFrame.SetInfo(jsonObj)
        self.MMRLayout.addWidget(mmrFrame.mmrItemFrame)

    def run_thread(self, api_factory, method, callback, *args):
        runnable = APICallRunnable(api_factory, method, *args)
        runnable.signals.result.connect(callback)
        runnable.signals.error.connect(self.on_error_occurred)
        self.thread_pool.start(runnable)

    def on_error_occurred(self, error):
        print(f"Error: {error}")
        self.AddMMRFrame(None)
        self.playerIdx += 1
        self.UpdateData(self.nickname_list)

    def API_GetPlayerMMRInfo(self, playerID):
        self.factory = APIFactory()
        self.run_thread(self.factory, "get_user_data", self.on_MMR_Data_Recive, playerID, self.factory.get_current_seasonId())
        print(playerID)

    def on_MMR_Data_Recive(self, data):
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

            self.AddMMRFrame(playerJsonObj)
            self.playerIdx += 1
            self.UpdateData(self.nickname_list)

class mmrUI(QWidget, mmrUisrc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def SetInfo(self, jsonObj):
        if jsonObj == None:
            self.charimage.setPixmap(QPixmap(":/char/CharIcon/193.png").scaled(self.charimage.size(), Qt.KeepAspectRatio))
            self.tierimage.setPixmap(QPixmap(":/char/CharIcon/196.png").scaled(self.tierimage.size(), Qt.KeepAspectRatio))
            self.nickname.setText("Not Found")
            self.winLate.setText("  승률: --")
            self.mmr.setText("  MMR: --")

            self.totalGame.setText("게임 수: --")
            self.avgRank.setText("평균 순위: --")
            self.avgKill.setText("평균 Kill: --")
            self.avgTK.setText("평균 TK: --")

            self.charGame.setText("플레이 횟수: --")
            self.charWinlate.setText("승률: --")
            self.charAvgRank.setText("평균 순위: --")
            return
        
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    #window.UpdateData(['한동그라미', '삼다수는맛있어', '커리'])
    #window.showMinimized()
    #window.showNormal()
    sys.exit(app.exec_())