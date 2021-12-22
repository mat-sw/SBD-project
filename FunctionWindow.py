from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class FunctionWindow(QWidget):
    def __init__(self):
        super(FunctionWindow, self).__init__()
        # self.initialze_grid()
        # self.setup()

    def initialze_grid(self):
        self.main_grid = QVBoxLayout()
        self.add_buttons()
        for button in [self.add, self.delete, self.modify, self.show]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")
        self.main_grid.addWidget(self.add, 0, 0)
        self.main_grid.addWidget(self.delete, 0, 1)
        self.main_grid.addWidget(self.modify, 1, 0)
        self.main_grid.addWidget(self.show, 1, 1)

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def add_buttons(self):
        self.add = QPushButton("Dodaj", self)
        self.delete = QPushButton("Usuń dane", self)
        self.modify = QPushButton("Modyfikuj dane", self)
        self.show = QPushButton("Wyświetl dane", self)

    def choose(self):
        pass