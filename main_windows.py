from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import numpy as np

width = 1000
height = 600
pos = np.array([1920/2 - width/2, 1080/2 - height/2])
size = np.array([width, height])


class Login_window(QWidget):
    def __init__(self):
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
        self.setup(pos, size/2, "Login Screen")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:  # enter
            self.authorize()
        else:
            self.infoLabel.setVisible(False)

    # def closeEvent(self, event):
    #     odp = QMessageBox.question(
    #         self, 'Komunikat',
    #         "Czy na pewno chcesz wyjść?",
    #         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #
    #     if odp == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def authorize(self):
        if self.loginLine.text() == 'admin' and self.passLine.text() == 'admin':
            self.goToMainWindow()
        else:
            self.infoLabel.setVisible(True)

    def goToMainWindow(self):
        self.window = Main_Window()
        self.window.show()
        self.close()


class Main_Window(QWidget):
    def __init__(self, parent = None):
        super(Main_Window, self).__init__(parent)
        my_grid = QVBoxLayout()
        info_line = QHBoxLayout()
        first_line = QHBoxLayout()
        second_line = QHBoxLayout()
        third_line = QHBoxLayout()
        info_label = QLabel("Wybierz co byś chciał modyfikować", self)
        info_label.setAlignment(Qt.AlignCenter)
        wyloguj = QPushButton("Wyloguj się", self)
        wyloguj.setCheckable(True)
        bilet = QPushButton("&Bilety", self)
        bilet.setCheckable(True)
        kierowca = QPushButton("&Kierowcy (Motorniczy)", self)
        kierowca.setCheckable(True)
        pojazd = QPushButton("&Pojazdy", self)
        pojazd.setCheckable(True)
        przystanek = QPushButton("P&rzystanki", self)
        przystanek.setCheckable(True)
        miasto = QPushButton("&Miasta", self)
        miasto.setCheckable(True)
        strefa = QPushButton("&Strefy", self)
        strefa.setCheckable(True)
        linia = QPushButton("&Linie", self)
        linia.setCheckable(True)
        model = QPushButton("M&odele pojazdu", self)
        model.setCheckable(True)
        biletomat = QPushButton("Biletomaty", self)
        biletomat.setCheckable(True)
        kasa = QPushButton("Kasy biletowe", self)
        kasa.setCheckable(True)
        producent = QPushButton("Producenci pojazdu", self)
        producent.setCheckable(True)
        gdzie = QPushButton("&Gdzie kupować bilet", self)
        gdzie.setCheckable(True)
        my_grid.addWidget(info_label)
        first_line.addWidget(bilet)
        first_line.addWidget(gdzie)
        first_line.addWidget(biletomat)
        first_line.addWidget(kasa)
        second_line.addWidget(pojazd)
        second_line.addWidget(model)
        second_line.addWidget(producent)
        second_line.addWidget(kierowca)
        third_line.addWidget(linia)
        third_line.addWidget(przystanek)
        third_line.addWidget(strefa)
        third_line.addWidget(miasto)
        my_grid.addLayout(first_line)
        my_grid.addLayout(second_line)
        my_grid.addLayout(third_line)
        self.setLayout(my_grid)
        self.setup(pos, size/2, "Main menu")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.goToLoginWindow()
        elif e.key() == Qt.Key_Return:  # enter
            pass
        else:
            self.infoLabel.setVisible(False)

    def closeEvent(self, event):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno chcesz się wylogować?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if odp == QMessageBox.Yes:
            self.goToLoginWindow()
            event.accept()
        else:
            event.ignore()

    def choose(self):
        pass

    def goToLoginWindow(self):
        self.window = Login_window()
        self.window.show()
        self.close()

    def goToCityWindow(self):
        pass

    def goToDrivertWindow(self):
        pass

    def goToLinesWindow(self):
        pass

    def goToModelWindow(self):
        pass

    def goToProducersWindow(self):
        pass

    def goToStopsWindow(self):
        pass

    def goToTicketWindow(self):
        pass

    def goToTicketOfficeWindow(self):
        pass

    def goToTicketMachineWindow(self):
        pass

    def goToVehiclesWindow(self):
        pass

    def goToWhereWindow(self):
        pass

    def goToZonesWindow(self):
        pass
