from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import numpy as np
from function_windows import *

width = 1000
height = 600
pos = np.array([1920 / 2 - width / 2, 1080 / 2 - height / 2])
size = np.array([width, height])


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        my_grid = QVBoxLayout()
        info_grid = QHBoxLayout()

        self.add_buttons()

        info_grid.addWidget(self.loginLabel)
        info_grid.addWidget(self.infoLabel)
        my_grid.addLayout(info_grid)
        my_grid.addWidget(self.loginLine)
        my_grid.addWidget(self.passLabel)
        my_grid.addWidget(self.passLine)
        my_grid.addWidget(self.loginButt)
        self.loginButt.clicked.connect(self.authorize)
        self.setLayout(my_grid)
        self.setup(pos, size / 2, "Login Screen")

    def add_buttons(self):
        self.loginLine = QLineEdit()
        self.loginLine.setProperty("mandatoryField", True)
        self.passLine = QLineEdit()
        self.passLine.setEchoMode(QLineEdit.Password)
        self.passLine.setProperty("mandatoryField", True)
        self.loginLabel = QLabel('Wpisz login:')
        self.infoLabel = QLabel('Niepoprawne dane!\nSpróbuj zalogować się jeszcze raz')
        self.passLabel = QLabel('Wpisz hasło:')
        self.loginButt = QPushButton('Zaloguj')
        self.loginButt.setCheckable(True)
        self.infoLabel.setVisible(False)
        self.infoLabel.setStyleSheet(" background-color: rgb(145, 252, 255); color: rgb(0, 0, 0);")
        self.infoLabel.setAlignment(Qt.AlignCenter)

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
        self.window = MainWindow()
        self.window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        my_grid = QVBoxLayout()
        info_line = QHBoxLayout()
        first_line = QHBoxLayout()
        second_line = QHBoxLayout()
        third_line = QHBoxLayout()

        self.add_buttons()

        for button in [self.bilet, self.gdzie, self.biletomat, self.kasa, self.pojazd, self.model, self.producent, self.kierowca, self.linia, self.przystanek,
                       self.strefa, self.miasto]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")

        info_line.addWidget(self.info_label)
        info_line.addWidget(self.wyloguj)
        first_line.addWidget(self.bilet)
        first_line.addWidget(self.gdzie)
        first_line.addWidget(self.biletomat)
        first_line.addWidget(self.kasa)
        second_line.addWidget(self.pojazd)
        second_line.addWidget(self.model)
        second_line.addWidget(self.producent)
        second_line.addWidget(self.kierowca)
        third_line.addWidget(self.linia)
        third_line.addWidget(self.przystanek)
        third_line.addWidget(self.strefa)
        third_line.addWidget(self.miasto)

        self.choose()

        for layout in [info_line, first_line, second_line, third_line]:
            my_grid.addLayout(layout)
        self.setLayout(my_grid)
        self.setup(pos, size * 2 / 3, "Main menu")

    def add_buttons(self):
        self.info_label = QLabel("Wybierz co byś chciał modyfikować", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-weight: bold; font-size : 10pt")
        self.wyloguj = QPushButton("Wyloguj się", self)
        self.wyloguj.setCheckable(True)
        self.wyloguj.setStyleSheet(" background-color: rgb(195, 238, 146); font-size : 10pt")
        self.bilet = QPushButton("&Bilety", self)
        self.bilet.setCheckable(True)
        self.kierowca = QPushButton("&Kierowcy (Motorniczy)", self)
        self.kierowca.setCheckable(True)
        self.pojazd = QPushButton("&Pojazdy", self)
        self.pojazd.setCheckable(True)
        self.przystanek = QPushButton("P&rzystanki", self)
        self.przystanek.setCheckable(True)
        self.miasto = QPushButton("&Miasta", self)
        self.miasto.setCheckable(True)
        self.strefa = QPushButton("&Strefy", self)
        self.strefa.setCheckable(True)
        self.linia = QPushButton("&Linie", self)
        self.linia.setCheckable(True)
        self.model = QPushButton("M&odele pojazdu", self)
        self.model.setCheckable(True)
        self.biletomat = QPushButton("Biletomaty", self)
        self.biletomat.setCheckable(True)
        self.kasa = QPushButton("Kasy biletowe", self)
        self.kasa.setCheckable(True)
        self.producent = QPushButton("Producenci pojazdu", self)
        self.producent.setCheckable(True)
        self.gdzie = QPushButton("&Gdzie kupować bilet", self)
        self.gdzie.setCheckable(True)

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
        self.wyloguj.setChecked(False)
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
        self.bilet.clicked.connect(self.goToTicketWindow)
        self.kierowca.clicked.connect(self.goToDriverWindow)
        self.gdzie.clicked.connect(self.goToWhereWindow)
        self.biletomat.clicked.connect(self.goToTicketMachineWindow)
        self.kasa.clicked.connect(self.goToTicketOfficeWindow)
        self.pojazd.clicked.connect(self.goToVehiclesWindow)
        self.model.clicked.connect(self.goToModelWindow)
        self.producent.clicked.connect(self.goToProducersWindow)
        self.linia.clicked.connect(self.goToLinesWindow)
        self.przystanek.clicked.connect(self.goToStopsWindow)
        self.strefa.clicked.connect(self.goToZonesWindow)
        self.miasto.clicked.connect(self.goToCityWindow)
        self.wyloguj.clicked.connect(self.close)

    def goToLoginWindow(self):
        self.window = LoginWindow()
        self.close()
        self.window.show()

    def goToCityWindow(self):
        self.window = City(pos + 50, size / 2)
        self.window.show()
        self.miasto.setChecked(False)

    def goToDriverWindow(self):
        self.window = Driver(pos + 50, size / 2)
        self.window.show()
        self.kierowca.setChecked(False)

    def goToLinesWindow(self):
        self.window = Line(pos + 50, size / 2)
        self.window.show()
        self.linia.setChecked(False)

    def goToModelWindow(self):
        self.window = Model(pos + 50, size / 2)
        self.window.show()
        self.model.setChecked(False)

    def goToProducersWindow(self):
        self.window = Producent(pos + 50, size / 2)
        self.window.show()
        self.producent.setChecked(False)

    def goToStopsWindow(self):
        self.window = Stop(pos + 50, size / 2)
        self.window.show()
        self.przystanek.setChecked(False)

    def goToTicketWindow(self):
        self.window = Tickets(pos + 50, size / 2)
        self.window.show()
        self.bilet.setChecked(False)

    def goToTicketOfficeWindow(self):
        self.window = TicketOffice(pos + 50, size / 2)
        self.window.show()
        self.kasa.setChecked(False)

    def goToTicketMachineWindow(self):
        self.window = TicketMachine(pos + 50, size / 2)
        self.window.show()
        self.biletomat.setChecked(False)

    def goToVehiclesWindow(self):
        self.window = Vehicle(pos + 50, size / 2)
        self.window.show()
        self.pojazd.setChecked(False)

    def goToWhereWindow(self):
        self.window = Where(pos + 50, size / 2)
        self.window.show()
        self.gdzie.setChecked(False)

    def goToZonesWindow(self):
        self.window = Zone(pos + 50, size / 2)
        self.window.show()
        self.strefa.setChecked(False)
