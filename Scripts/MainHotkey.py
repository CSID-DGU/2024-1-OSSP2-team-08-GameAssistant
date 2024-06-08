import sys
import pyautogui



from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from pynput.keyboard import Listener, Key, KeyCode

class HotkeyListener(QtCore.QThread):
    hotkey_pressed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.store = set()
        self.hot_key = set([Key.alt_l, KeyCode(char='d')])
        self.json_data = []
        self.capture_helper_ui = None

    def handleKeyPress(self, key):
        self.store.add(key)

    def handleKeyRelease(self, key):
        check = all([True if k in self.store else False for k in self.hot_key])
        if check:
            self.hotkey_pressed.emit()

        if key in self.store:
            self.store.remove(key)

        if key == Key.esc:
            return False

    def run(self):
        with Listener(on_press=self.handleKeyPress, on_release=self.handleKeyRelease) as listener:
            listener.join()
            
    def onHotkeyPressed(self):
        if self.capture_helper_ui is None:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
    def getjson(self):
        return self.json_data