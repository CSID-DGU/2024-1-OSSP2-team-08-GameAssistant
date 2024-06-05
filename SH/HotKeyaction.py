from pynput.keyboard import Listener, Key, KeyCode
import pyautogui
import api
from NicknameCapture import NicknameCapture
from MainUI import MainUI
import mmrUItest

store = set()
hot_key = set([Key.alt_l, KeyCode(char='d')])

def handleKeyPress( key ):
    store.add( key )

def autoclick():
    # x = 85
    # y = 140
    # pyautogui.moveto(x, y).click()
    MainUI.display(3)

def handleKeyRelease( key ):
    check = all([True if k in store else False for k in hot_key ])
    if check:
        print("aa")
        autoclick()
        capture=NicknameCapture('./SaveDate.json', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        img_list = capture.capture_images()
        name_list = capture.get_nicknames(img_list)
        api_factory = api.APIFactory('./api_init_data.json')
        for nickname in name_list:
            match_data = api_factory.get_match_data(nickname) #api에서 가져온 정보 반환됨, ui파일 위치 지정 필요
            matchui = mmrUItest.mmrUI()
            matchui.setInfo(match_data) # mmrui.ui에 정보 저장, IngameMMR에 배정된 ui에 add
            matchui.show()
                      
          
    if key in store:
        store.remove( key )

    # 종료
    if key == Key.esc:
        return False

def start_hot_key():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()


start_hot_key()
