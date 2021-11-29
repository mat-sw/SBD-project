from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import Qt
import numpy as np

width = 1000
heigth = 600
middle_of_screen = np.array([1920/2 - width/2, 1080/2 - heigth/2])


class Main_Window(QWidget):
    def __init__(self, parent = None):
        super(Main_Window, self).__init__(parent)
        label = QLabel("Sub Window",  self)
        my_grid = QVBoxLayout()
        self.setup(middle_of_screen, [400, 300], "Main menu")


    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def closeEvent(self, event):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno chcesz się wylogować?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def choose(self):
        pass