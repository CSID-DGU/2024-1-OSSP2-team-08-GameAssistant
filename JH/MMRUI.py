import sys, os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from mmrUItest import mmrUI

MainUiSource = uic.loadUiType("Data/UI/MainUI/Main.ui")[0]

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
