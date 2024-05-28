import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

MatchUi_Sample = uic.loadUiType("./teamui.ui")[0]
    
class APIconnect(QWidget, MatchUi_Sample):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def json_PlayerInfo(self, json_root):
        with open(json_root, 'r') as f:
            jsonObj = json.load(f)
            accessCode = jsonObj["code"]
            Message = jsonObj["message"]
            playerId = jsonObj["user"]["userNum"]
            Nickname = jsonObj["user"]["nickname"]

            userRank = jsonObj["userRank"]["rank"]
            userMMR = jsonObj["userRank"]["mmr"]
            
            selectgame = jsonObj["userGames"]["gamdId"] #게임에 부여된 고유 번호
            result = jsonObj["userGames"]["gameRank"]
            matchTime = jsonObj["userGames"]["playTime"]
            teamKill = jsonObj["userGames"]["teamKill"]
            playerKill = jsonObj["userGames"]["playerKill"]
            playerDeath = jsonObj["userGames"]["playerDeaths"]
            playerAssistant = jsonObj["userGames"]["playerAssistant"]
            playerDMG = jsonObj["userGames"]["damageToPlayer"]
            playerMMRBefore = jsonObj["userGames"]["mmrBefore"]
            playerMMRAfter = jsonObj["userGames"]["mmrAfter"]
            playerCharcode = jsonObj["userGames"]["characterNum"] #실험체의 번호
            
            playerName = jsonObj["userRank"]["nickname"]
            playerMMR = jsonObj["userRank"]["mmr"]
            WinorDefeat = jsonObj["userGames"]["victory"] #승리 여부, playerWin + playerLose
        
            self.rank_label.setText(result)
            self.charcode_label.setPixmap(QPixmap("./" + playerCharcode + ".png")) #이미지 파일 경로지정
            self.nickname_label.setText(Nickname)
            self.KDA_label.setText(teamKill + "/" + playerKill + "/" + playerDeath + "/" + playerAssistant)
            self.damage_label.setText(playerDMG)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    matchui = APIconnect()
    matchui.json_PlayerInfo("""json 파일 root""")
    matchui.show()
    app.exec_()