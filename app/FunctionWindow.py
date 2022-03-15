from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QTableWidget, QLabel
from PyQt5.QtCore import Qt


class FunctionWindow(QWidget):
    def __init__(self):
        super(FunctionWindow, self).__init__()
        self.updatesEnabled()

    def add_buttons(self):
        self.push_button = QPushButton("Dodaj")
        self.push_button.setCheckable(True)

    def setup(self, pos, size, title):
        self.setGeometry(1920 / 2 - size[0] / 2, 1080 / 2 - size[1] / 2, size[0], size[1])
        self.setWindowTitle(title)

    def initialze_grid(self):
        self.main_grid = QGridLayout()
        self.view = QTableWidget()
        self.info_label = QLabel()
        self.info_label.setStyleSheet("background-color: rgb(145, 252, 255); color: rgb(255, 0, 0); font-size : 14pt;")
        self.info_label.setVisible(False)
        self.add_buttons()
        self.main_grid.addWidget(self.view, 0, 0)
        self.main_grid.addWidget(self.info_label, 1, 0)
        self.setLayout(self.main_grid)

    def get_signal(self):
        self.view.clicked.connect(self.modify)
        self.push_button.clicked.connect(self.add_to_db)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            self.add_to_db()
