from pynput.mouse import Listener
from pynput.keyboard import GlobalHotKeys as HotKeys
from pynput.keyboard import Controller
from image_fix import masking_image
import pyautogui as pygui
import json

from PIL import Image
import pytesseract

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
    def __init__(self, json_file_path, image_folder_path, tesseract_file_path):
        self.__start_pos = []
        self.__end_pos = []
        self.__json_file_path = json_file_path #get file path as parameter
        self.__image_folder_path = image_folder_path #get image folder path as parameter
        pytesseract.pytesseract.tesseract_cmd = tesseract_file_path #tesseract .exe path
        self.__image_list = []
        self.__region_list= []
        self.__load_json()

        
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

    def start_hotkey(self):
        with HotKeys({
        '<shift>+s': self.on_capture_image_button}) as h:
            h.join()

    def on_click(self, x, y, button, pressed): #get region and add in __region_list
        if pressed:
            print('on_pressed') #test, delete after
            self.__start_pos.append(x)
            self.__start_pos.append(y)
        if not pressed:
            print('on_release') #test, delete after
            self.__end_pos.append(x)
            self.__end_pos.append(y)
            self.__region_list.append(Region("", self.__start_pos, self.__end_pos))
            return False

    
    def on_activate_drag(self): #start setting region
        print('on_act_start') #test, delete after
        with Listener(on_click=self.on_click) as l:
            l.join()

        return False

    def save_json(self):
        print('on_save') #test, delete after
        json_data = []
        for reg in self.__region_list:
            dic = reg.get_dict()
            json_data.append(dic)

        with open(self.__json_file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)


    def on_capture_image_button(self):
        self.capture_images()
        self.get_text_from_image()
        return False

        
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
            masking_image(img, [172,178, 165])
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

#testcode
capture=NicknameCapture("NicknameCapture/JSON/SaveDate.json", './capture_image/', r"C:\Program Files\Tesseract-OCR\tesseract.exe")

#capture when hotkey pressed
capture.start_hotkey()
