from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class Label(QLabel):
    def __init__(self, rgb, parent=None):
        super(Label, self).__init__(parent)
        self.setStyleSheet(" background-color: rgb({}, {}, {}); color: rgb(0, 0, 0);".format(rgb[0], rgb[1], rgb[2]))
        self.setFrameStyle(6)
