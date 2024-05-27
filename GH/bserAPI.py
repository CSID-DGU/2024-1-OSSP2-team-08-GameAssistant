from api import APIFactory

class bserAPIFactory(APIFactory):
    def get_user_data(self, nickname : str, seasonId : str):
        s=self._get_request_url("GetUserNumber", {'nickname':nickname})
        headers = { "accept" : "application/json", "x-api-key" : "fbTETbo0ur2sQe5bBTpin47qzJYQzk6M4R2jzWV4" }
        user_num=self._get_api_data(s, headers=headers).json()['user']['userNum']
        
        s=self._get_request_url("GetUserStats", {'userNum':user_num, 'seasonId': seasonId})
        user_stats=self._get_api_data(s, headers=headers).json()['userStats'][0]

        return { 'nickname' : user_stats['nickname'], 'mmr' : user_stats['mmr'],\
                 'totalGames':user_stats['totalGames'], 'totalWins' : user_stats['totalWins']}
    
        
    def get_match_data(self, nickname : str):
        s=self._get_request_url("GetUserNumber", {'nickname':nickname})
        headers = { "accept" : "application/json", "x-api-key" : "fbTETbo0ur2sQe5bBTpin47qzJYQzk6M4R2jzWV4" }
        user_num=self._get_api_data(s, headers=headers).json()['user']['userNum']

        s=self._get_request_url("GetUserGames", { 'userNum' : user_num})
        user_matches=self._get_api_data(s, headers=headers).json()['userGames']
        match_data_list = []
        for match in user_matches:
            death = match['playerDeaths']
            if death == 0:
                death=1
            kda= (match['playerKill'] + match['playerAssistant']) / death

            mmrBefore = match['mmrBefore'] if 'mmrBefore' in match else 0
            mmrAfter = match['mmrAfter'] if 'mmrAfter' in match else 0
            
            match_data_list.append({ 'kda' : kda, 'damageToPlayer': match['damageToPlayer'],\
              'mmrBefore' : mmrBefore, 'mmrAfter' : mmrAfter,\
              'gameRank' : match['gameRank'], 'playTime': match['playTime']})

        return match_data_list

    

file_link = r"./text.json"

a=bserAPIFactory(file_link)

r=a.get_user_data('한동그라미', '6')
print(r)
r=a.get_match_data('한동그라미')
print(r)

