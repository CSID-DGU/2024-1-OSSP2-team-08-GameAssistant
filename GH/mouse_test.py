from pynput.mouse import Listener
from pynput.keyboard import GlobalHotKeys as HotKeys
from pynput.keyboard import Controller
import pyautogui as pygui

point_list = []

def on_click(x, y, button, pressed):
    print('on_click')
    if pressed:
        global start_pos
        start_pos = [x, y]
    if not pressed:
        global end_pos
        end_pos = [x, y]
        point_list.append((start_pos+end_pos))
        print(point_list)
        return False

def on_activate_drag():
    #shift + d
    print('on_act_start')
    with Listener(on_click=on_click) as l:
        l.join()

def on_save_images():
    #shift + s
    print('on_save')
    i=0
    for [x1, y1, x2, y2] in point_list:
        width=abs(x1 - x2)D
        height=abs(y1 - y2)
        if width==0 | height==0:
            print("Wrong range")
            continue
        print(x1, x2, y1, y2)
        pygui.screenshot('./capture_image/test' + str(i) + '.png',\
                     region=(x1 if x1<x2 else x2,
                             y1 if y1<y2 else y2,
                             width, height))
        i+=1

with HotKeys({
        '<shift>+d': on_activate_drag,
        '<shift>+s': on_save_images}) as h:
    h.join()
