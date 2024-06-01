import requests
import json

def json_PlayerInfo(json_root):
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
    
# result = "gameRank" #등수 혹은 승리여부
# matchTime = "playTime" #경기 시간
# playerKill = "playerKill" #플레이어의 킬수
# playerDeath = "PlayerDeaths" #플레이어의 데스 수
# playerAssistant = "playerAssistant" #플레이어의 어시스트 수
# playerDMG = "damageToPlayer" #플레이어가 준 데미지
# playerMMRBefore = "mmrBefore" #이전 MMR
# playerMMRAfter = "mmrAfter" #이후 MMR
# playerCharCode = "characterCode"

# playerCharCode = "characterCode"
# playerName = "playerName"
# playerMMR = "playerMMR"
# playerWin = "playerWin"
# playerLose = "playerLose"