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
'''
MMRUIWindowSource = uic.loadUiType("Data/UI/MMRUI/MMRUI3P.ui")[0]
MMRJsonPath = "Data/TestJson/playersMMR/Player"
'''
class MMRWindowUI(QMainWindow, MMRUIWindowSource):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialized = False

    def initialize(self):
        if not self.initialized:
            for i in range(1, 4):
                self.AddMMRFrame(MMRJsonPath+str(i)+".json")
            self.initialized = True

    def AddMMRFrame(self, jsonPath):
        mmrFrame = mmrUI()
        mmrFrame.setInfo(jsonPath)
        self.MMRLayout.addWidget(mmrFrame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MMRWindowUI()
    window.initialize()
    window.show()
    sys.exit(app.exec_())
