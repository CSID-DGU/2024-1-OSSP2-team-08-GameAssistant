import json

class APIFactory:
    def __init__(self, file_link):
        self.__file_link=file_link

    def get_api_func(self, func_name, **args):
        data={}
        try:
            with open(self.__file_link) as f:
                data = json.load(f)
        except Exception as e:
            print(f"{e}")

        if func_name in data:
            return data[func_name].format(**args)
        else:
            return None


a=APIFactory(r"C:\Users\신기환\OneDrive\Desktop\동국대 수업\2024년 1학기\공개SW프로젝트\text.json")

dic={"seasonId" : "1", "matchingTeamMode" : "12"}

print(a.get_api_func("GetUserNumber", nickname="한동그라미"))
print(a.get_api_func("TopRankers", **dic))


