from PyQt5.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self, rgb=(255, 255, 255), parent=None):
        super(Label, self).__init__(parent)
        self.setStyleSheet(" background-color: rgb({}, {}, {}); color: rgb(0, 0, 0);".format(rgb[0], rgb[1], rgb[2]))
