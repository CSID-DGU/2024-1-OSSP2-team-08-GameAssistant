from pynput.mouse import Listener
from pynput.keyboard import GlobalHotKeys as HotKeys
from pynput.keyboard import Controller
import pyautogui as pygui
import json

class Region:
    def __init__(self, start_pos, end_pos):
        self.name = ""
        self.region = [0, 0, 0, 0]
        self.region[0] = start_pos[0] #x1
        self.region[1] = start_pos[1] #y1
        self.region[2] = end_pos[0] #x2
        self.region[3] = end_pos[1] #y2

    def get_width(self):
        return abs(self.region[0] - self.region[2])

    def get_height(self):
        return abs(self.region[1] - self.region[3])

    def get_dict(self):
        return {"name" : self.name, "region" : self.region}

    def set_name(self, name):
        self.name = name
          
region_list = []

def save_json(json_data):
    file_path = "./Regions.json"
    try:
        with open(file_path, "r") as json_file:
            prev_data = json.load(json_file)        
    except FileNotFoundError:
        #when no file
        with open(file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)
        
    except json.decoder.JSONDecodeError:
        #when wrong json
        print("WRONG JSON FILE!")
    else:
        #insert mouse position data    
        new_data = prev_data + json_data
        with open(file_path, 'w') as outfile:
            json.dump(new_data, outfile, indent=2)

def on_click(x, y, button, pressed):
    print('on_click')
    if pressed:
        global start_pos
        start_pos = [x, y]
    if not pressed:
        global end_pos
        end_pos = [x, y]
        region_list.append(Region(start_pos, end_pos))
        return False

def on_activate_drag():
    #shift + d
    print('on_act_start')
    with Listener(on_click=on_click) as l:
        l.join()

def on_save_json():
    #shift + s
    print('on_save')
    json_data = []
    for reg in region_list:
        dic = reg.get_dict()
        json_data.append(dic)
        print(json_data)

    save_json(json_data)

with HotKeys({
        '<shift>+d': on_activate_drag,
        '<shift>+s': on_save_json}) as h:
    h.join()
  
