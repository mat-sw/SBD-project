from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class Login_window(QWidget):
    def __init__(self, pos, size):
        super(Login_window, self).__init__()
        my_grid = QVBoxLayout()
        info_grid = QHBoxLayout()
        self.loginLine = QLineEdit()
        self.passLine = QLineEdit()
        self.loginLabel = QLabel('Wpisz login:')
        self.infoLabel = QLabel('Niepoprawne dane!\nSpróbuj zalogować się jeszcze raz')
        self.passLabel = QLabel('Wpisz hasło:')
        self.loginButt = QPushButton('Zaloguj')
        self.loginButt.setCheckable(True)
        self.infoLabel.setVisible(False)
        self.infoLabel.setStyleSheet(" background-color: rgb(145, 252, 255); color: rgb(0, 0, 0);")
        self.infoLabel.setAlignment(Qt.AlignCenter)
        # self.loginLine.setToolTip('Wpisz login')
        # self.passLine.setToolTip('Wpisz haslo')
        info_grid.addWidget(self.loginLabel)
        info_grid.addWidget(self.infoLabel)
        my_grid.addLayout(info_grid)
        my_grid.addWidget(self.loginLine)
        my_grid.addWidget(self.passLabel)
        my_grid.addWidget(self.passLine)
        my_grid.addWidget(self.loginButt)
        self.loginButt.clicked.connect(self.authorize)
        self.setLayout(my_grid)
        self.setup(pos, [400, 300], "Login Screen")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:  # enter
            self.authorize()

    def closeEvent(self, event):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno chcesz wyjść?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def authorize(self):
        if self.loginLine.text() == 'admin' and self.passLine.text() == 'admin':
            self.close()

        else:
            self.infoLabel.setVisible(True)
