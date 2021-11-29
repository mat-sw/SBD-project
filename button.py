from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QAbstractButton


class Button(QPushButton):
    def __init__(self, rgb, parent=None):
        super(Button, self).__init__(parent)
        self.setStyleSheet("background-color: rgb({}, {}, {}); color: rgb(0, 0, 0);".format(rgb[0], rgb[1], rgb[2]))

