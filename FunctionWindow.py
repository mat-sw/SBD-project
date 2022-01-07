from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QTableWidget
from PyQt5.QtCore import Qt


class FunctionWindow(QWidget):
    def __init__(self):
        super(FunctionWindow, self).__init__()

    def add_buttons(self):
        # self.add = QPushButton("Dodaj nowy rekord", self)
        self.push_button = QPushButton("Dodaj")
        self.push_button.setCheckable(True)

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def initialze_grid(self):
        self.main_grid = QGridLayout()
        self.view = QTableWidget()
        self.add_buttons()
        self.main_grid.addWidget(self.view, 0, 0)
        self.setLayout(self.main_grid)

    def choose(self):
        pass

    def get_signal(self):
        self.view.clicked.connect(self.fun_del)
        # self.add.clicked.connect(self.fun_add)
        self.push_button.clicked.connect(self.add_to_db)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
