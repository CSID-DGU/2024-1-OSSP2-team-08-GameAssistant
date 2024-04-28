import sys
import json
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter, QColor

ImgSelectWindowSource = uic.loadUiType("NicknameCapture/UI/SelectImg.ui")[0]
CaptureHelperSource = uic.loadUiType("NicknameCapture/UI/CaptureHelper.ui")[0]

class ImgSelectUI(QWidget, ImgSelectWindowSource):
    def __init__(self):
        super().__init__()
        self.fpath = ""

        self.setupUi(self)
        self.findFileButton.clicked.connect(self.Btn_FindFile)
        self.nextButton.clicked.connect(self.Btn_Next)

    def Btn_FindFile(self):
        fname = QFileDialog.getOpenFileName(self,'','',"Image(*.png *.jpg)")
        if fname[0]:
            self.fpath = fname[0]
            self.fileLocationLadel.setText(self.fpath)
            self.sampleImgFrame.setStyleSheet("QFrame { border-image: url('"+ self.fpath +"');}")
        return
    
    def Btn_Next(self):
        if self.fpath != "":
            self.other_window  = CaptureHelperUI(self.fpath) #통합 시 수정 필요
            self.other_window.showFullScreen()
            self.hide()
        else: # for Debug
            self.other_window  = CaptureHelperUI(self.fpath) 
            self.other_window.showFullScreen()
            self.hide()
        return

class CaptureHelperUI(QWidget, CaptureHelperSource):
    def __init__(self, fpath):
        super().__init__()
        self.setupUi(self)
        self.NicknameCaptureFrame.setStyleSheet("QFrame { border-image: url('"+ fpath +"');}")

        self.createButton.clicked.connect(self.Btn_Create)
        self.editButton.clicked.connect(self.Btn_Edit)
        self.saveButton.clicked.connect(self.Btn_Save)
        self.exitButton.clicked.connect(self.Btn_Exit)
        self.sectionNameOK.clicked.connect(self.Btn_EnterName)
        self.sectionNameFrame.hide()

        self.start_point = None
        self.end_point = None

        self.__file_path = "./Regions.json"
        self.__region_list= []
        #self.__load_json()

        class State(Enum):
            Normal = 0
            Creat = 1
            EnterName = 2
            Edit = 3
            Save = 4
        self.state = State(0)
        self.state = 0

    def Btn_Create(self):
        self.state = 1
        self.mainMenuFrame.hide()
        return

    def Btn_Edit(self):
        self.state = 3
        return
    
    def Btn_EnterName(self):
        name = self.sectionNameInput.text()
        self.__region_list.append(Region(name, [self.start_point.x(), self.start_point.y()], [self.end_point.x(), self.end_point.y()]))
        self.mainMenuFrame.show()
        self.sectionNameFrame.hide()
        self.state = 0

    def Btn_Save(self):
        self.state = 4
        return

    def Btn_Exit(self):
        self.close()

    def __load_json(self):
        try:
            with open(self.__file_path, "r") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            print("File not exist")
        except json.decoder.JSONDecodeError:
            #when wrong json
            print("WRONG JSON FILE!")
        else:
            for region in json_data:
                self.__region_list.append(Region(region["name"],\
                                          [region["region"][0], region["region"][1]],\
                                          [region["region"][2], region["region"][3]]))
                
            for region in self.__region_list:
                print(region.get_name(), region.get_region())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.state == 1:
            self.start_point = event.pos()
            self.end_point = None
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.state == 1:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.state == 1 :
            self.end_point = event.pos()
            self.state = 2
            self.sectionNameFrame.show()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(Qt.red))

        if self.start_point and self.end_point and (self.state == 1 or self.state == 2 ):          
            painter.drawRect(self.start_point.x(), self.start_point.y(),
                             self.end_point.x() - self.start_point.x(),
                             self.end_point.y() - self.start_point.y())
        
        for obj in self.__region_list:
            pos = obj.get_region()
            painter.drawRect(pos[0], pos[1],
                            pos[2] - pos[0],
                            pos[3] - pos[1])


class Region:
    def __init__(self, name, start_pos, end_pos):
        self.__name = name
        self.__region = [0, 0, 0, 0]
        self.__region[0] = start_pos[0] #x1
        self.__region[1] = start_pos[1] #y1
        self.__region[2] = end_pos[0] #x2
        self.__region[3] = end_pos[1] #y2

    def get_width(self):
        return abs(self.__region[0] - self.__region[2])

    def get_height(self):
        return abs(self.__region[1] - self.__region[3])

    def get_dict(self):
        return {"name" : self.__name, "region" : self.__region}

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name
    
    def get_region(self):
        return self.__region



if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    ImgSelectObj = ImgSelectUI()
    ImgSelectObj.show()

    app.exec_()