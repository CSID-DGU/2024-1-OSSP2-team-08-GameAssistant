from pynput.mouse import Listener
from pynput.keyboard import GlobalHotKeys as HotKeys
from pynput.keyboard import Controller
#from image_fix import masking_image
import pyautogui as pygui
import json
import os

from PIL import Image
import pytesseract
json_file_path = "Data/Json/captureJson/Regions.json"

class Region: #json region struct
    def __init__(self, name, start_pos, end_pos):
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

class NicknameCapture:
    def __init__(self):
        self.__start_pos = []
        self.__end_pos = []
        self.__json_file_path = json_file_path #get file path as parameter
        self.tesseract_file_path = self.find_tesseract_installation()
        if self.tesseract_file_path == None:
            print("Can find tesseract")
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_file_path #tesseract .exe path
        self.__image_list = []
        self.__region_list= []
        self.__load_json()

    def find_tesseract_installation(self):
        # Windows의 일반적인 설치 경로 확인
        if os.name == "nt":
            standard_install_paths = [
                r"C:\Program Files\Tesseract-OCR",
                r"C:\Program Files (x86)\Tesseract-OCR"
            ]
            for path in standard_install_paths:
                if os.path.exists(path):
                    return os.path.join(path, "tesseract.exe")
            else:
                return None
        # 다른 운영 체제
        else:
            return None
        
    def __load_json(self): #load json data from file at init
        try:
            with open(self.__json_file_path, "r") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            #when no file
            print("File not exist")
        except json.decoder.JSONDecodeError:
            #when wrong json
            print("WRONG JSON FILE!")
        else:
            for region in json_data:
                self.__region_list.append(Region(region["name"],\
                                          [region["region"][0], region["region"][1]],\
                                          [region["region"][2], region["region"][3]]))
                
            for region in self.__region_list:
                print(region.get_name(), region.get_region()) #test, delete after


    def OCR_Nickname(self):
        self.capture_images()
        return self.get_text_from_image()

        
    def capture_images(self): #capture all images in region
        print('on_save_image') #test, delete after
        image_list=[]
        for idx, region in enumerate(self.__region_list):

            width=region.get_width()
            height=region.get_height()
            rect = region.get_region()
            if(width == 0 | height == 0): #continue if wrong region
                continue
            #capture image
            #rect = [x1, y1, x2, y2]
            #path/image0.png, path/image1.png ...
            img = pygui.screenshot(region=(rect[0] if rect[0]<rect[2] else rect[2],\
                                     rect[1] if rect[1]<rect[3] else rect[3],
                                     width, height))
            #masking_image(img, [172,178, 165])
            image_list.append(img)

        self.__image_list = image_list

    def get_text_from_image(self):
        nickname_list=[]
        for idx, region in enumerate(self.__region_list):
            text = pytesseract.image_to_string(self.__image_list[idx], lang='kor+eng',config='--psm 7')
            text=text[:-1] # delete \n
            dic=dict(name = region.get_name(), nickname=str(text))
            nickname_list.append(dic)
        print(nickname_list) #for test
        return nickname_list
    
#testcodeS
# capture=NicknameCapture("NicknameCapture/JSON/SaveDate.json", './capture_image/', r"C:\Program Files\Tesseract-OCR\tesseract.exe")

#capture when hotkey pressed
# capture.start_hotkey()
