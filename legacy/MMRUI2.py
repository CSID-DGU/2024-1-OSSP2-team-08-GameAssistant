import sys, os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from mmrUItest import mmrUI

current_dir = os.path.dirname(__file__)
ui_file_path1 = os.path.join(current_dir, '..', 'Data', 'UI', 'MMRUI', 'MMRUI3P.ui')
ui_file_path1 = os.path.abspath(ui_file_path1)

json_file_path = os.path.join(current_dir, '..', 'Data', 'TestJson', 'playersMMR', 'Player')
json_file_path = os.path.abspath(json_file_path)

MMRUIWindowSource = uic.loadUiType(ui_file_path1)[0]
MMRJsonPath = json_file_path

Nicknames = ["닉네임1", "닉네임2", "닉네임3"]
'''
MMRUIWindowSource = uic.loadUiType("Data/UI/MMRUI/MMRUI3P.ui")[0]
MMRJsonPath = "Data/TestJson/playersMMR/Player"
'''
class MMRWindowUI(QMainWindow, MMRUIWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialized = False

    def initialize(self, Nicknames):
        if not self.initialized:
            for nickname in Nicknames:
                self.AddMMRFrame(nickname)
            self.initialized = True

    def AddMMRFrame(self, nickname):
        mmrFrame = mmrUI()
        mmrFrame.setInfo(nickname)
        self.MMRLayout.addWidget(mmrFrame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    window.initialize(Nicknames)
    window.show()
    sys.exit(app.exec_())