from PyQt5.QtWidgets import QPushButton

class Button(QPushButton):
    def __init__(self, rgb=(255, 255, 255), parent=None):
        super(Button, self).__init__(parent)
        self.setStyleSheet("background-color: rgb({}, {}, {}); color: rgb(0, 0, 0);".format(rgb[0], rgb[1], rgb[2]))

