import sys, os
import json
from enum import Enum
from PyQt5.QtCore import Qt,QDir
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPainter, QColor

if getattr(sys, 'frozen', False):
    Data_path = QDir.currentPath() + '/Data'
else:
    Data_path = 'Data'

current_dir = os.path.dirname(__file__)
ui_file_path1 = Data_path +'/UI/NickNameCapture/SelectImg.ui'
ui_file_path2 = Data_path + '/UI/NickNameCapture/CaptureHelper.ui'
json_file_path = Data_path + '/Json/captureJson/Regions.json'

ImgSelectWindowSource = uic.loadUiType(ui_file_path1)[0]
CaptureHelperSource = uic.loadUiType(ui_file_path2)[0]


class ImgSelectUI(QWidget, ImgSelectWindowSource):
    def __init__(self):
        super().__init__()
        self.fpath = ""

        self.setupUi(self)
        self.findFileButton.clicked.connect(self.Btn_FindFile)
        self.nextButton.clicked.connect(self.Btn_Next)

    def Btn_FindFile(self):
        fname = QFileDialog.getOpenFileName(self, '', '', "Image(*.png *.jpg)")
        if fname[0]:
            self.fpath = fname[0]
            self.fileLocationLadel.setText(self.fpath)
            self.sampleImgFrame.setStyleSheet("QFrame { border-image: url('" + self.fpath + "');}")
        return

    def Btn_Next(self):
        if self.fpath != "":
            self.other_window = CaptureHelperUI(self.fpath)
            self.other_window.showFullScreen()
            self.hide()
        return


class CaptureHelperUI(QWidget, CaptureHelperSource):
    def __init__(self, fpath):
        super().__init__()
        self.setupUi(self)
        self.pixmap = QPixmap(fpath)

        self.createButton.clicked.connect(self.Btn_Create)
        self.editButton.clicked.connect(self.Btn_Edit)
        self.saveButton.clicked.connect(self.Btn_Save)
        self.exitButton.clicked.connect(self.Btn_Exit)
        self.resetButton.clicked.connect(self.Btn_Reset)
        self.sectionNameOK.clicked.connect(self.Btn_EnterName)
        self.sectionNameFrame.hide()

        self.start_point = None
        self.end_point = None
        self.selected_region = None

        self.__file_path = json_file_path  # Correct file path for regions
        self.__region_list = []
        self.__load_json()

        class State(Enum):
            Normal = 0
            Create = 1
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
        self.mainMenuFrame.hide()
        return

    def Btn_EnterName(self):
        name = self.sectionNameInput.text()
        if name == "":
            return

        if self.state == 3 and self.selected_region:
            # Edit the name of the selected region
            self.selected_region.set_name(name)
            self.save_json()  # Save changes to the JSON file after renaming
            self.selected_region = None
        else:
            # Create a new region
            self.__region_list.append(
                Region(name, [self.start_point.x(), self.start_point.y()], [self.end_point.x(), self.end_point.y()]))

        self.mainMenuFrame.show()
        self.sectionNameFrame.hide()
        self.state = 0
        self.update()

    def Btn_Save(self):
        self.save_json()
        return

    def Btn_Exit(self):
        self.close()

    def Btn_Reset(self):
        self.__region_list.clear()
        self.save_json()
        self.update()

    def __load_json(self):
        try:
            with open(self.__file_path, "r") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            print("File not exist")
        except json.decoder.JSONDecodeError:
            print("WRONG JSON FILE!")
        else:
            for region in json_data:
                self.__region_list.append(Region(region["name"], \
                                                 [region["region"][0], region["region"][1]], \
                                                 [region["region"][2], region["region"][3]]))

            for region in self.__region_list:
                print(region.get_name(), region.get_region())

    def save_json(self):
        json_data = []
        for reg in self.__region_list:
            dic = reg.get_dict()
            json_data.append(dic)

        with open(self.__file_path, 'w') as outfile:  # Save to json_file_path
            json.dump(json_data, outfile, indent=2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.state == 1:
            self.start_point = event.pos()
            self.end_point = None
            self.update()
        elif event.button() == Qt.LeftButton and self.state == 3:
            self.selected_region = self.get_region_at(event.pos())
            if self.selected_region:
                self.contextMenu(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.state == 1:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.state == 1:
            self.end_point = event.pos()
            self.state = 2
            self.sectionNameFrame.show()
            self.sectionNameInput.setFocus()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

        painter.setPen(QColor(Qt.red))
        if self.start_point and self.end_point and (self.state == 1 or self.state == 2):
            painter.drawRect(self.start_point.x(), self.start_point.y(),
                             self.end_point.x() - self.start_point.x(),
                             self.end_point.y() - self.start_point.y())

        for obj in self.__region_list:
            pos = obj.get_region()
            painter.drawRect(pos[0], pos[1],
                             pos[2] - pos[0],
                             pos[3] - pos[1])

    def contextMenu(self, pos):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        rename_action = menu.addAction("Rename")
        action = menu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            self.__region_list.remove(self.selected_region)
            self.save_json()  # Save changes to the JSON file after deletion
            self.selected_region = None
            self.update()
            self.mainMenuFrame.show()
        elif action == rename_action:
            self.sectionNameFrame.show()
            self.sectionNameInput.setText(self.selected_region.get_name())  # Pre-fill the input with the current name
            self.sectionNameInput.setFocus()
            self.state = 3  # Set state to Edit mode for renaming
            self.update()

    def get_region_at(self, pos):
        for region in self.__region_list:
            rect = region.get_region()
            if rect[0] <= pos.x() <= rect[2] and rect[1] <= pos.y() <= rect[3]:
                return region
        return None

class Region:
    def __init__(self, name, start_pos, end_pos):
        self.__name = name
        self.__region = [start_pos[0], start_pos[1], end_pos[0], end_pos[1]]

    def get_width(self):
        return abs(self.__region[0] - self.__region[2])

    def get_height(self):
        return abs(self.__region[1] - self.__region[3])

    def get_dict(self):
        return {"name": self.__name, "region": self.__region}

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ImgSelectObj = ImgSelectUI()
    ImgSelectObj.show()

    app.exec_()