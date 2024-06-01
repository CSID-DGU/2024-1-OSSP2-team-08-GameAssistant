import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

DefaultFrame = uic.loadUiType("MatchInfoFrame.ui")[0]
RecordStructure = uic.loadUiType("printInfoWidget.ui")[0]

class MatchJsonInfo():
    #Set Here
    isWinOrLose = False

    #Set Json Names
    playerCharCode = "serialNumber" #계정 일련번호
    characterCode = "characterCode" #캐릭터 정보
    playerName = "playerName" #닉네임
    result = "gameRank" #등수 혹은 승리여부
    spellD = "playerSpellD" #플레이어 사용 스펠D
    spellF = "playerSpellF" #플레이어 사용 스펠F
    playerKill = "playerKill" #플레이어의 킬수
    playerDeath = "playerDeath" #플레이어의 데스 수
    playerAssistant = "playerAssistant" #플레이어의 어시스트 수

# class PlayerJsonInfo():
#     playerCharCode = "characterCode"
#     playerName = "playerName"
#     playerWin = "playerWin"
#     playerLose = "playerLose"

class GameRecord(QMainWindow, DefaultFrame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def AddUi(self, playerId, OpponentId):
        recordui = RecordUi()
        recordui.SetInfo(recordui.Openjson(playerId))
        recordui.setOppoInfo(recordui.OpenOpjson(OpponentId))
        self.RecordWidget.addWidget(recordui)

class RecordUi(QWidget, RecordStructure):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def SetInfo(self, jsonObj):
        self.serialNum = jsonObj[MatchJsonInfo.playerCharCode]
        self.characterName = jsonObj[MatchJsonInfo.characterCode]
        self.Nickname = jsonObj[MatchJsonInfo.playerName]
        self.playerRank = jsonObj[MatchJsonInfo.result]
        self.spellD = jsonObj[MatchJsonInfo.spellD]
        self.spellF = jsonObj[MatchJsonInfo.spellF]
        self.playerKill = jsonObj[MatchJsonInfo.playerKill]
        self.playerDeath = jsonObj[MatchJsonInfo.playerDeath]
        self.playerAssistant = jsonObj[MatchJsonInfo.playerAssistant]
        
        self.IPicture.setPixmap(QPixmap(("imagefile\\" + str(self.characterName) + ".png")))
        self.nickname.setText(self.Nickname)
        self.spellDloc.setPixmap(QPixmap(("imagefile\\" + self.spellD + ".png")).scaled(36, 36))
        self.spellFloc.setPixmap(QPixmap(("imagefile\\" + self.spellF + ".png")).scaled(36, 36))
        self.KDA.setText(str(self.playerKill) + "/" + str(self.playerDeath) + "/" + str(self.playerAssistant))
        #self.KDA.setStyleSheet("font-size: 8pt")
        return
    
    def setOppoInfo(self, jsonObj):
        self.serialNum = jsonObj[MatchJsonInfo.playerCharCode]
        self.characterName = jsonObj[MatchJsonInfo.characterCode]
        self.Nickname = jsonObj[MatchJsonInfo.playerName]
        self.playerRank = jsonObj[MatchJsonInfo.result]
        self.spellD = jsonObj[MatchJsonInfo.spellD]
        self.spellF = jsonObj[MatchJsonInfo.spellF]
        self.playerKill = jsonObj[MatchJsonInfo.playerKill]
        self.playerDeath = jsonObj[MatchJsonInfo.playerDeath]
        self.playerAssistant = jsonObj[MatchJsonInfo.playerAssistant]
        
        self.IPicture_2.setPixmap(QPixmap(("imagefile\\" + str(self.characterName) + ".png")))
        self.nickname_2.setText(self.Nickname)
        self.spellDloc_2.setPixmap(QPixmap(("imagefile\\" + self.spellD + ".png")).scaled(36, 36))
        self.spellFloc_2.setPixmap(QPixmap(("imagefile\\" + self.spellF + ".png")).scaled(36, 36))
        self.KDA_2.setText(str(self.playerKill) + "/" + str(self.playerDeath) + "/" + str(self.playerAssistant))
    
    def Openjson(self, playerID):
        file = open("test" + str(playerID) + ".json", 'r', encoding='utf-8')
        jsonObjfile = json.load(file)
        return jsonObjfile
    
    def OpenOpjson(self, OpponentID):
        file = open("testopponent" + str(OpponentID) + ".json", 'r', encoding='utf-8')
        jsonObjfile = json.load(file)
        return jsonObjfile
        
        # self.eximage = QPixmap("imagefile\challenger.png")
        # self.sTeleport = QPixmap("imagefile\Teleport.png")
        # self.sFlash = QPixmap("imagefile\Flash.png")
        # self.IPicture.setPixmap(self.eximage.scaled(120, 80))
        # self.ISpell1 = QLabel()
        # self.ISpell2 = QLabel()
        # self.ISpell1.setPixmap(self.sTeleport.scaled(36, 36))
        # self.ISpell1.setContentsMargins(3, 7, 3, 4)
        # self.ISpell2.setPixmap(self.sFlash.scaled(36, 36))
        # self.ISpell2.setContentsMargins(3, 4, 3, 7)
        # self.SpellBox.addWidget(self.ISpell1)
        # self.SpellBox.addWidget(self.ISpell2)    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = GameRecord()
    myWindow.AddUi(1, 1)
    myWindow.resize(1300, 750)
    myWindow.show()
    app.exec_()