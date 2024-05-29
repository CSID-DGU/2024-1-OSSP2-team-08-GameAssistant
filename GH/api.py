import json
import requests
from urllib import parse

class APIFactory:
    def __init__(self, file_link: str):
        self.__file_link=file_link
        try:
            f=open(self.__file_link)
        except Exception as e:
            raise e
        
        try:
            self.__init_data = json.load(f)
        except Exception as e:
            f.close()
            raise e

        f.close()

        try:
            self.__api_key=self.__init_data['api_key']
            self.__base_url=self.__init_data['base_url']
        except Exception as e:
            raise e

    #make request url
    #args mapped into json data
    def _get_request_url(self, func_name: str, url_args: dict , encode : bool = False) -> str:
        #encode text to url encoding
        if encode:
            for key, val in url_args.items():
                url_args[key] = parse.quote(val)

        #return request url
        if func_name in self.__init_data:
            return self._make_url(func_name, url_args)
        else:
            return None

    #can be overrided
    def _make_url(self, func_name : str, url_args : dict):
        return self.__base_url + self.__init_data[func_name].format(**url_args)

    def _get_api_data(self, request_url : str, params : dict = None, headers : dict = None, cookies : dict = None):

        r=requests.get(request_url, headers = headers)
        #raise error if wrong status
        r.raise_for_status()
            
        return r

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




