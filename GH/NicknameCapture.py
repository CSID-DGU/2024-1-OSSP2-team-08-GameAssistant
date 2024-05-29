import pyautogui as pygui
import json
from PIL import Image
import pytesseract

class Region: #json region struct
    def __init__(self, name : str, start_pos : list, end_pos : list):
        self.__name = name
        self.__region = [0, 0, 0, 0]
        self.__region[0] = start_pos[0] #x1
        self.__region[1] = start_pos[1] #y1
        self.__region[2] = end_pos[0] #x2
        self.__region[3] = end_pos[1] #y2

    def get_width(self):
        return abs(self.__region[0] - self.__region[2])

    def get_height(self):
        return abs(self.__region[1] - self.__region[3])

    def get_dict(self):
        return {"name" : self.__name, "region" : self.__region}

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name
    
    def get_region(self):
        return self.__region

    def get_start_pos(self): #get left-up point of rect
        return [self.__region[0] if self.__region[0] < self.__region[2] else self.__region[2]\
                , self.__region[1] if self.__region[1] < self.__region[3] else self.__region[3]]

class NicknameCapture:    
    def __init__(self, json_file_path : str, tesseract_file_path:str):
        self.__start_pos = []
        self.__end_pos = []
        self.__json_file_path = json_file_path #get file path as parameter
        self.__region_list= []
        pytesseract.pytesseract.tesseract_cmd = tesseract_file_path
        self.__load_json()

        
    def __load_json(self): #load json data from file at init
        try:
            with open(self.__json_file_path, "r") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError as e:
            #when no file
            raise e
        except json.decoder.JSONDecodeError as e:
            #when wrong json
            raise e
        
        for region in json_data:
            self.__region_list.append(Region(region["name"],\
                                        [region["region"][0], region["region"][1]],\
                                        [region["region"][2], region["region"][3]]))
        
    def capture_images(self): #capture all images in region
        image_list=[]
        for idx, region in enumerate(self.__region_list):
            width=region.get_width()
            height=region.get_height()
            start_pos = region.get_start_pos()
            if(width == 0 | height == 0): #continue if wrong region
                continue
            #capture image
            #rect = [x1, y1, x2, y2]
            #path/image0.png, path/image1.png ...
            img = pygui.screenshot(region=(start_pos[0], start_pos[1], width, height))
            image_list.append(img)

        return image_list

    #OCR CODE
    def __fix_image(self):
        return

    #get nickname from Image list
    def get_nicknames(self, image_list : list):
        nickname_list=[]
        for img in image_list:
            nickname=pytesseract.image_to_string(img, lang='kor+eng',config='--psm 7').strip()
            nickname_list.append(nickname)
        return nickname_list



NicknameCapture('./SaveDate.json', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
