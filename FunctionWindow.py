from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt



class FunctionWindow(QWidget):
    def __init__(self):
        super(FunctionWindow, self).__init__()

    def add_buttons(self):
        self.add = QPushButton("Dodaj", self)
        self.delete = QPushButton("Usuń dane", self)
        self.modify = QPushButton("Modyfikuj dane", self)
        self.show_button = QPushButton("Wyświetl dane", self)

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def initialze_grid(self):
        self.main_grid = QGridLayout()
        self.add_buttons()
        for button in [self.add, self.delete, self.modify, self.show_button]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")
        self.main_grid.addWidget(self.add, 0, 0)
        self.main_grid.addWidget(self.delete, 0, 1)
        self.main_grid.addWidget(self.modify, 1, 0)
        self.main_grid.addWidget(self.show_button, 1, 1)
        self.setLayout(self.main_grid)

    def choose(self):
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()