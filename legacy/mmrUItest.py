import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap




        
if __name__ == "__main__":
     app = QApplication(sys.argv)
     
     mmrui = mmrUI()
     mmrui.setInfo("text.json")
     mmrui.show()
     
     app.exec_()