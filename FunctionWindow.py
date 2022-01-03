from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QTableWidget
from PyQt5.QtCore import Qt



class FunctionWindow(QWidget):
    def __init__(self):
        super(FunctionWindow, self).__init__()

    def add_buttons(self):
        self.add = QPushButton("Dodaj", self)

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def initialze_grid(self):
        self.main_grid = QGridLayout()
        self.view = QTableWidget()
        self.add_buttons()
        self.main_grid.addWidget(self.view, 0, 0)
        self.main_grid.addWidget(self.add, 1, 0)
        self.setLayout(self.main_grid)

    def choose(self):
        pass

    # def get_signal(self):
    #     self.view.clicked.connect(self.func_test)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()