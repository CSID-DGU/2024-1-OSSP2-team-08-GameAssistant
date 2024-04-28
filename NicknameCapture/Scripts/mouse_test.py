from pynput.mouse import Listener
from pynput.keyboard import GlobalHotKeys as HotKeys
from pynput.keyboard import Controller
import pyautogui as pygui
import json

class Region:
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
        self.__file_path = "./Regions.json"
        self.__region_list= []
        self.__load_json()

        
    def __load_json(self):
        try:
            with open(self.__file_path, "r") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
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
                print(region.get_name(), region.get_region())

    def start_hotkey(self):
        with HotKeys({
        '<shift>+d': self.on_activate_drag,
        '<shift>+s': self.on_save_json}) as h:
            h.join()

    def on_click(self, x, y, button, pressed):    
        if pressed:
            print('on_pressed')
            self.__start_pos.append(x)
            self.__start_pos.append(y)
        if not pressed:
            print('on_release')
            self.__end_pos.append(x)
            self.__end_pos.append(y)
            self.__region_list.append(Region("", self.__start_pos, self.__end_pos))
            return False

    
    def on_activate_drag(self):
        #shift + d
        print('on_act_start')
        with Listener(on_click=self.on_click) as l:
            l.join()

        return False

    def on_save_json(self):
        #shift + s
        print('on_save')
        json_data = []
        for reg in self.__region_list:
            dic = reg.get_dict()
            json_data.append(dic)

        with open(self.__file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)

        return False


a=NicknameCapture()
a.start_hotkey()
  
