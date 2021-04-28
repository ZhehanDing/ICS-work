
from PyQt5.QtGui import *

from PyQt5.QtWidgets import *
import PyQt5.QtCore as PQC



class PushButton(QLabel):
    click_signal = PQC.pyqtSignal()

    def __init__(self, imagepaths, parent=None, **kwargs):
        super(PushButton, self).__init__(parent)
        self.image_0 = QPixmap(imagepaths[0])
        self.image_1 = QPixmap(imagepaths[1])
        self.image_2 = QPixmap(imagepaths[2])
        self.resize(self.image_0.size())
        self.setPixmap(self.image_0)
        #self.setMask(self.image_1.mask())

    def enterEvent(self, event):
        self.setPixmap(self.image_1)



    def leaveEvent(self, event):
        self.setPixmap(self.image_0)


    def mousePressEvent(self, event):
        if event.button() == PQC.Qt.LeftButton:

            self.setPixmap(self.image_2)

    def mouseReleaseEvent(self, event):
        if event.button() == PQC.Qt.LeftButton:

            self.setPixmap(self.image_1)
            self.click_signal.emit()