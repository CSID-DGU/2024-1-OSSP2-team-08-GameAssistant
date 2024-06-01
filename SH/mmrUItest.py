import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

mmrUisrc = uic.loadUiType("mmrUI.ui")[0]

class mmrUI(QWidget, mmrUisrc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setInfo(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            jsonObj = json.load(f)

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
        
if __name__ == "__main__":
     app = QApplication(sys.argv)
     
     mmrui = mmrUI()
     mmrui.setInfo("text.json")
     mmrui.show()
     
     app.exec_()