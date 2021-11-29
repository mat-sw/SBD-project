from PyQt5 import QtWidgets
#, QtCore, QtGui
# from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from button import Button
from label import Label
from line_edit import Line_Edit

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # self.button = Button(self)
        # self.label = Label(self)
        # self.line_edit = Line_Edit(self)
        self.my_grid = QtWidgets.QGridLayout()

    def setup(self, pos, width, heigth, title):
        self.setGeometry(pos[0], pos[1], width, heigth)
        self.setWindowTitle(title)

    def add_label(self, text, pos, size, rgb=(255, 255, 255)):
        self.label = Label(rgb, self)
        self.label.setText(text)
        self.label.move(pos[0], pos[1])
        self.label.setLineWidth(50)
        # self.label.setFrameStyle(10)
        # self.my_grid.addWidget(self.label)

    def add_button(self, text, pos, rgb=(255, 255, 255)):
        self.button = Button(rgb, self)
        self.button.setText(text)
        self.button.move(pos[0], pos[1])

    def add_line_edit(self, text, pos, rgb=(255, 255, 255)):
        self.line_edit = Line_Edit(rgb, self)
        self.line_edit.setText(text)
        # self.text_edit.resize(100, 25)
        self.line_edit.move(pos[0], pos[1])
        # self.line_edit.setAlignment(Qt.AlignCenter) # alignment