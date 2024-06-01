from pynput.keyboard import Listener, Key, KeyCode
import api
from NicknameCapture import NicknameCapture
from NicknameOCR import NicknameOCR
import textaction

store = set()
hot_key = set([Key.alt_l, KeyCode(char='s')])

def handleKeyPress( key ):
    store.add( key )
 
def handleKeyRelease( key ):
    check = all([True if k in store else False for k in hot_key ])
    if check:
        print("aa")
        capture=NicknameCapture('./SaveDate.json', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        img_list = capture.capture_images()
        name_list = capture.get_nicknames(img_list)
        api_factory = api.APIFactory('./api_init_data.json')
        match_data=api_factory.get_match_data(name_list[0])
        app = textaction.QApplication(textaction.sys.argv)
        matchui = textaction.APIconnect()
        matchui.json_PlayerInfo(match_data[0])
        matchui.show()
        app.exec_()
        
              
          
    if key in store:
        store.remove( key )

    # 종료
    if key == Key.esc:
        return False

def start_hot_key():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()


start_hot_key()
