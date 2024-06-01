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
        
    def json_PlayerInfo(self, jsonObj):
        result = jsonObj["gameRank"]
        playerCharcode = jsonObj["characterNum"] #실험체의 번호
        Nickname = jsonObj["nickname"]
        teamKill = jsonObj["teamKill"]
        playerKill = jsonObj["playerKill"]
        playerDeath = jsonObj["playerDeaths"]
        playerAssistant = jsonObj["playerAssistant"]
        playerDMG = jsonObj["damageToPlayer"]
    
        self.rank_label.setText(str(result))
        self.charcode_label.setPixmap(QPixmap("./" + str(playerCharcode) + ".png")) #이미지 파일 경로지정
        self.nickname_label.setText(Nickname)
        self.KDA_label.setText(str(teamKill) + "/" + str(playerKill) + "/" + str(playerDeath) + "/" + str(playerAssistant))
        self.damage_label.setText(str(playerDMG))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    matchui = APIconnect()
    matchui.show()
    app.exec_()
