import sys, os
import json
import api
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
#from mmrUItest import mmrUI

mmrUisrc = uic.loadUiType("../Data/UI/MMRUI/mmrUI.ui")[0]
MMRUIWindowSource = uic.loadUiType("../Data/UI/MMRUI/MMRUI3P.ui")[0]

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
        user_stats = jsonObj["userStats"][0]
        Charactercode = user_stats["characterStats"][0]["characterCode"]
        Nickname = user_stats["nickname"]
        rankPoint = user_stats["mmr"]
        rankNum = user_stats["rank"]
        userTotal = user_stats["totalGames"]
        userWin = user_stats["totalWins"]
        useravgRank = user_stats["averageRank"]
        useravgKill = user_stats["averageKills"]
        useravgAssistant = user_stats["averageAssistants"]
        
        # 첫 번째 캐릭터의 데이터 가져오기
        char_stats = user_stats["characterStats"][0]
        charUsage = char_stats["usages"]
        charTop3 = char_stats["top3"]
        chargameRank = char_stats["averageRank"]
        
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
        return data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    window.UpdateData(['한동그라미', '삼다수는맛있어', '커리'])
    window.show()
    sys.exit(app.exec_())
