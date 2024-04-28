import sys
import json
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

        self.start_point = None
        self.end_point = None

    def Btn_Create():
        return

    def Btn_Edit():
        return
    
    def Btn_Save():
        return

    def Btn_Exit(self):
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = None
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            self.update()

    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QColor(Qt.red))
            painter.drawRect(self.start_point.x(), self.start_point.y(),
                             self.end_point.x() - self.start_point.x(),
                             self.end_point.y() - self.start_point.y())
            print("Draw!")


if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    ImgSelectObj = ImgSelectUI()
    ImgSelectObj.show()

    app.exec_()