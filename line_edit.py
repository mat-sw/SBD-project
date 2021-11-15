from PyQt5.QtWidgets import QLineEdit

class Line_Edit(QLineEdit):
    def __init__(self, rgb=(255, 255, 255), parent=None):
        super(Line_Edit, self).__init__(parent)
        self.setStyleSheet("background-color: rgb({}, {}, {}); color: red;".format(rgb[0], rgb[1], rgb[2]))
