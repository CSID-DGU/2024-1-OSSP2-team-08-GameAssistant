import json
import requests
from urllib import parse
import time

init_data_path='../Data/TestJson/API/api_init_data.json'

class APIFactory:
    def __init__(self):
        self.__file_link=init_data_path
        try:
            f=open(self.__file_link)
        except Exception as e:
            print("[APIFactory.__init__()] : File Open Error")
            return
        
        try:
            self.__init_data = json.load(f)
        except Exception as e:
            f.close()
            print("[APIFactory.__init__()] : Json Load Error")
            return

        f.close()

        try:
            self.__api_key=self.__init_data['data']['api_key']
            self.__base_url=self.__init_data['data']['base_url']
        except Exception as e:
            print("[APIFactory.__init__()] : Key Error")
            return

    #make request url
    #args mapped into json data
    def _get_request_url(self, func_name: str, url_args: dict , encode : bool = False) -> str:
        #encode text to url encoding
        if encode:
            for key, val in url_args.items():
                url_args[key] = parse.quote(val)

        #return request url
        if func_name in self.__init_data['URL']:
            return self._make_url(func_name, url_args)
        else:
            return None

    #can be overrided
    def _make_url(self, func_name : str, url_args : dict):
        return self.__base_url + self.__init_data['URL'][func_name].format(**url_args)

    def _get_api_data(self, request_url : str, params : dict = None, headers : dict = None, cookies : dict = None):
        try:
            r=requests.get(request_url, headers = headers)
            time.sleep(1.5)
        except:
            print("[_get_api_data()] : requests.get Error")
            return None

        try:
            r=r.json()
        except:
            print("[_get_api_data()] : response to json Error")
            return None

        if r['code'] == 200:
            return r
        else:
            print("[get_user_data] : http code " + str(r['code']))
            return None

    def get_user_data(self, nickname : str, seasonId : str):
        #request url 생성
        s=self._get_request_url("GetUserNumber", {'nickname':nickname}, True)
        if s == None: #request url error
            print("[get_user_data()] : Wrong Request URL")

        #user num 받아오기
        headers = { "accept" : "application/json", "x-api-key" : self.__api_key }
        response=self._get_api_data(s, headers=headers)
        if response:
            user_num=response['user']['userNum']
        else: #api 호출 과정에서 에러가 발생한 경우
            print("[get_user_data()] : No Response")
            return None
        s=self._get_request_url("GetUserStats", {'userNum':user_num, 'seasonId': seasonId})
        if s == None: #request url error
            print("[get_user_data()] : Wrong Request URL")
        
        response=self._get_api_data(s, headers=headers)

        if response:
            return response
        else:
            print("[get_user_data()] : No Response")
            return None
  
        
    def get_match_data(self, nickname : str):
        s=self._get_request_url("GetUserNumber", {'nickname':nickname})
        if s == None: #request url error
            print("[get_user_data()] : Wrong Request URL")

        headers = { "accept" : "application/json", "x-api-key" : self.__api_key }
        response=self._get_api_data(s, headers=headers)
        if response:
            user_num=response['user']['userNum']
        else: #api 호출 과정에서 에러가 발생한 경우
            print("[get_user_data()] : No Response")
            return None

        s=self._get_request_url("GetUserGames", { 'userNum' : user_num})
        if s == None: #request url error
            print("[get_user_data()] : Wrong Request URL")
        response=self._get_api_data(s, headers=headers)
        
        if response:
            return response
        else:
            print("[get_user_data()] : No Response")
            return None

    #현재 시즌 번호 받아오기
    def get_current_seasonId(self):
        s=self._get_request_url("GetData", {'metaType': 'Season'})
        if s == None: #request url error
            print("[get_user_data()] : Wrong Request URL")

        headers = { "accept" : "application/json", "x-api-key" : self.__api_key }
        response=self._get_api_data(s, headers=headers)
        if response:
            for seasons in response['data']:
                if seasons['isCurrent'] == 1:
                    return seasons['seasonID']
        else: #api 호출 과정에서 에러가 발생한 경우
            print("[get_user_data()] : No Response")
            return None

