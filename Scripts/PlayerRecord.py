import sys, os
import json
from API.api import APIFactory, APICallRunnable, WorkerSignals
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QCursor

if getattr(sys, 'frozen', False):
    Data_path = QtCore.QDir.currentPath() + '/Data'
else:
    Data_path = 'Data'

RecordWindowSource = uic.loadUiType(Data_path+"/UI/Record/RecordFrame.ui")[0]
MatchScoreSource = uic.loadUiType(Data_path+"/UI/Record/MatchRecord.ui")[0]

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
    playerTK = "teamKill"

    default = {result : 0, matchTime : 0, playerKill : 0, playerDeath : -1, playerAssistant : 0,\
               playerDMG : 0, playerMMRBefore : 0, playerMMRAfter : 0, playerCharCode : 0, playerTK: 0}

class PlayerJsonInfo():
    playerCharCode = "characterCode"
    playerName = "nickname"
    playerMMR = "mmr"
    playerWin = "totalWins"
    playerLose = "playerLose"
    playerGames = "totalGames"
    playerAvgRank = "averageRank"

    default = {playerCharCode : 0, playerName : "", playerMMR : 0, \
               playerWin : 0, playerLose : 0, playerGames : -1, playerAvgRank: 1.0}

class RecordFrameUI(QWidget, RecordWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.MatchesLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollAreaWidgetContents_2.setLayout(self.MatchesLayout)

        self.NameSearch.clicked.connect(self.UpdateData)
        self.NameInput.returnPressed.connect(self.UpdateData)
        self.NameSearch.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.PlayerInfoFrame.hide()
        self.SearchIngFrame.hide()
        self.ErrorFrame.hide()

        self.thread_pool = QThreadPool()

        self.IsThreadRunning = False

    def SetPlayerInfo(self, jsonObj):
        playerCharCode = jsonObj[PlayerJsonInfo.playerCharCode]
        playerName = jsonObj[PlayerJsonInfo.playerName]
        playerMMR = jsonObj[PlayerJsonInfo.playerMMR]
        playerWin = jsonObj[PlayerJsonInfo.playerWin]
        playerGames = jsonObj[PlayerJsonInfo.playerGames]
        playerAvgRank = jsonObj[PlayerJsonInfo.playerAvgRank]

        self.Nickname.setText(playerName)
        self.PlayerMMR.setText("MMR: "+str(playerMMR))
        self.Winlate.setText(str(round(playerWin/(playerGames)*100,1))+"%")
        self.avgRank.setText("평균 순위: "+str(round(playerAvgRank, 1)))
        self.totalGame.setText("게임 수: "+str(playerGames))

        self.PlayerImg.setPixmap(QPixmap((":/champions/Champions/Mini/"+str(playerCharCode)+".png")))
        self.PlayerInfoFrame.show()
        return

    def AddMatchFrame(self, jsonObj):
        matchObj = MatchUI()
        matchObj.SetInfo(jsonObj)
        self.MatchesLayout.insertWidget(-1, matchObj.MatchFrame)

    def UpdateData(self):
            if self.IsThreadRunning:
                return
            else:
                self.IsThreadRunning = True
                self.SearchIngFrame.show()
                self.PlayerInfoFrame.hide()
                self.ErrorFrame.hide()
                usernameSrc = self.NameInput.text()
                self.get_player_data(usernameSrc)
                self.get_match_data(usernameSrc)
                self.SearchName.setText(usernameSrc)
                self.SearchName.setAlignment(Qt.AlignCenter)
            

    def run_thread(self, api_factory, method, callback, *args):
        runnable = APICallRunnable(api_factory, method, *args)
        runnable.signals.result.connect(callback)
        runnable.signals.error.connect(self.on_error_occurred)
        self.thread_pool.start(runnable)

    def on_player_data_received(self, data):
        if data == None:
            return None
        else:
            stats = [stats for stats in data['userStats'] if stats['matchingMode'] == 3]
            mmr=[]
            win=[]
            lose=[]
            games=[]
            avgRank=[]
            for stat in stats:
                mmr.append(stat['mmr'])
                win.append(stat['totalWins'])
                lose.append(stat['totalGames'] - stat['totalWins'])
                games.append(stat['totalGames'])
                avgRank.append(stat['averageRank'])

            #평균 계산
            mmr = round(sum(mmr)/len(mmr))
            win = sum(win)
            lose = sum(lose)
            games = sum(games)
            avgRank = sum(avgRank)
                            #솔로에서 가장 많이 쓴 캐릭터
            playerJsonObj = {PlayerJsonInfo.playerCharCode : data['userStats'][0]['characterStats'][0]['characterCode'], \
                            PlayerJsonInfo.playerName : data['userStats'][0]['nickname'], \
                            PlayerJsonInfo.playerMMR : mmr, \
                            PlayerJsonInfo.playerWin : win, \
                            PlayerJsonInfo.playerLose : lose, \
                            PlayerJsonInfo.playerGames : games, \
                            PlayerJsonInfo.playerAvgRank: avgRank}
        self.SetPlayerInfo(playerJsonObj)

    def on_match_data_received(self, data):
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
                                    MatchJsonInfo.playerCharCode : match['characterNum'], \
                                    MatchJsonInfo.playerTK: match['teamKill']    }
                    match_info_list.append(matchJsonObj)
        for i in range(1, 20 if len(match_info_list) > 20 else len(match_info_list)):
            self.AddMatchFrame(match_info_list[i])
        self.IsThreadRunning = False
        self.SearchIngFrame.hide()
        self.ErrorFrame.hide()

    def on_error_occurred(self, error):
        print(f"Error: {error}")
        self.ErrorFrame.show()
        self.SearchIngFrame.hide()
        self.IsThreadRunning = False

    def get_player_data(self, usernameSrc):
        self.factory = APIFactory()
        self.run_thread(self.factory, "get_user_data", self.on_player_data_received, usernameSrc, self.factory.get_current_seasonId())

    def get_match_data(self, usernameSrc):
        while self.MatchesLayout.count() > 0:  # Keep the spacer
            item = self.MatchesLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.MatchesLayout.addItem(self.spacer)
        self.factory = APIFactory()
        self.run_thread(self.factory, "get_match_data", self.on_match_data_received, usernameSrc)

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
        playerTK = jsonObj[MatchJsonInfo.playerTK]

        tmpColor = ""
        if playerRank == 1:
            tmpColor = "rgb(17,178,136)"
        elif playerRank == 2 or playerRank == 3:
            tmpColor = "blue"
        else:
            tmpColor = "rgb(153,153,153)"
        self.Result.setText("<span style='color: white; font-size:18px;'>"+str(playerRank) + "위")   
        self.Result.setAlignment(Qt.AlignCenter)
        
        
        self.MatchTime.setText(str(matchTime//60)+"분 "+str(matchTime%60)+"초")
        self.KDA.setText("<span style='font-size:19px;'>"+str(playerKill)+" / "+"<span style='color: red;'>"+str(playerDeath)+"</span>"+" / "+str(playerAssistant)+"</span>")
        self.KDALate.setText("<span style='font-size:15px;'>"+"KDA: "+ ("Perfact" if playerDeath == 0 else str(round((playerKill+playerAssistant)/playerDeath,1)))+"</span>")
        self.DMG.setText("<span style='font-size:15px;'>"+"DMG: "+str(playerDMG)+"</span>")
        self.TK.setText("<span style='font-size:15px;'>"+"TK: "+str(playerTK)+"</span>")

        if playerMMRGain > 0:
            self.MMR.setText("<span style='font-size:15px;'>"+"MMR: "+str(playerMMRAfter)+"<span style='color: red;'> ▲"+str(playerMMRGain)+"</span>"+"</span>")
        else:
            self.MMR.setText("<span style='font-size:15px;'>"+"MMR: "+str(playerMMRAfter)+"<span style='color: blue;'> ▼"+str(-playerMMRGain)+"</span>"+"</span>")
        
        
        self.CharIMG.setPixmap(QPixmap((":/champions/Champions/Mini/"+str(playerCharCode)+".png")))


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    
    recordFrameObj = RecordFrameUI()
    recordFrameObj.show()
    
    app.exec_()
