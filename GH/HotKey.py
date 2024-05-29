from pynput.keyboard import Listener, Key, KeyCode
import api
from NicknameCapture import NicknameCapture
from NicknameOCR import NicknameOCR

store = set()
hot_key = set([Key.alt_l, KeyCode(char='s')])

def handleKeyPress( key ):
    store.add( key )
 
def handleKeyRelease( key ):
    check = all([True if k in store else False for k in hot_key ])
    if check:
        capture=NicknameCapture('./SaveDate.json', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        img_list = capture.capture_images()
        name_list = capture.get_nicknames(img_list)
        api_factory = api.APIFactory('./api_init_data.json')
        player_data_list=[]
        match_data_list=[]
        for name in name_list:
            player_data_list.append(api_factory.get_user_data(name, '6'))
            match_data_list.append(api_factory.get_match_data(name))

        print(player_data_list)
        print(match_data_list)
              
          
    if key in store:
        store.remove( key )

    # 종료
    if key == Key.esc:
        return False

def start_hot_key():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()


start_hot_key()
