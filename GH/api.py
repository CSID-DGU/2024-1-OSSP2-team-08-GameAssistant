import json
import requests
from urllib import parse

class APIFactory:
    def __init__(self, file_link, api_key, base_link):
        self.__file_link=file_link
        self.api_key = api_key
        self.base_link = base_link

    def get_request_url(self, func_name, **args):
        data={}
        try:
            with open(self.__file_link) as f:
                data = json.load(f)
        except Exception as e:
            print(f"{e}")

        for key, val in args.items():
            args[key] = parse.quote(val)
        
        if func_name in data:
            return self.base_link + data[func_name].format(**args)
        else:
            return None


file_link = r"C:\Users\신기환\OneDrive\Desktop\동국대 수업\2024년 1학기\공개SW프로젝트\text.json"
api_key = "fbTETbo0ur2sQe5bBTpin47qzJYQzk6M4R2jzWV4"
base_link = "https://open-api.bser.io/"

a=APIFactory(file_link, api_key, base_link)

url = a.get_request_url("GetUserNumber", nickname="한동그라미")

headers = { "accept" : "application/json", "x-api-key" : "fbTETbo0ur2sQe5bBTpin47qzJYQzk6M4R2jzWV4" }
    
r = requests.get(url, headers=headers)

print(r.json())
