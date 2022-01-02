from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui
from function_windows import *


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.my_grid = QVBoxLayout()
        self.info_grid = QHBoxLayout()
        self.add_buttons()

        self.info_grid.addWidget(self.loginLabel)
        self.info_grid.addWidget(self.infoLabel)
        self.my_grid.addLayout(self.info_grid)
        self.my_grid.addWidget(self.loginLine)
        self.my_grid.addWidget(self.passLabel)
        self.my_grid.addWidget(self.passLine)
        self.my_grid.addWidget(self.loginButt)
        self.loginButt.clicked.connect(self.authorize)
        self.setLayout(self.my_grid)
        self.setup(pos, size / 2, "Ekran logowania")

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
            # self.goToMainWindow()
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
            conn = connect_db()
            self.goToMainWindow(conn)
        else:
            self.infoLabel.setVisible(True)

    def goToMainWindow(self, conn):
        self.window = MainWindow(conn)
        self.window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, conn, parent=None):
        super(MainWindow, self).__init__(parent)
        self.conn = conn
        self.my_grid = QGridLayout()
        self.add_buttons()

        for button in [self.bilet, self.gdzie, self.biletomat, self.kasa, self.pojazd, self.model,
                       self.producent, self.kierowca, self.linia, self.przystanek, self.strefa, self.miasto]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")
            button.setMinimumSize(QSize(160, 30))

        self.my_grid.addWidget(self.wyloguj, 0, 3, Qt.AlignCenter)
        self.my_grid.addWidget(self.info_label, 1, 0, 1, 4, Qt.AlignHCenter)

        for i, button in enumerate([self.bilet, self.gdzie, self.biletomat, self.kasa]):
            self.my_grid.addWidget(button, 2, i, Qt.AlignCenter)
        for i, button in enumerate([self.pojazd, self.model, self.producent, self.kierowca]):
            self.my_grid.addWidget(button, 3, i, Qt.AlignCenter)
        for i, button in enumerate([self.linia, self.przystanek, self.strefa, self.miasto]):
            self.my_grid.addWidget(button, 4, i, Qt.AlignCenter)

        self.my_grid.setSpacing(20)
        self.choose()
        self.setLayout(self.my_grid)
        self.setup(pos, size * 2 / 3, "Główne menu")

    def add_buttons(self):
        self.info_label = QLabel("Wybierz co chciałbyś modyfikować", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-weight: bold; font-size : 10pt")
        self.wyloguj = QPushButton("Wyloguj się", self)
        self.wyloguj.setCheckable(True)
        self.wyloguj.setStyleSheet(" background-color: rgb(195, 238, 146); font-size : 10pt")
        self.bilet = QPushButton("&Bilety", self)
        self.kierowca = QPushButton("&Kierowcy (Motorniczy)", self)
        self.pojazd = QPushButton("&Pojazdy", self)
        self.przystanek = QPushButton("P&rzystanki", self)
        self.miasto = QPushButton("&Miasta", self)
        self.strefa = QPushButton("&Strefy", self)
        self.linia = QPushButton("&Linie", self)
        self.model = QPushButton("M&odele pojazdu", self)
        self.biletomat = QPushButton("Biletomaty", self)
        self.kasa = QPushButton("Kasy biletowe", self)
        self.producent = QPushButton("Producenci pojazdu", self)
        self.gdzie = QPushButton("&Gdzie kupować bilet", self)

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
        self.window = City(self.conn)
        self.window.show()

    def goToDriverWindow(self):
        self.window = Driver(self.conn)
        self.window.show()

    def goToLinesWindow(self):
        self.window = Line(self.conn)
        self.window.show()

    def goToModelWindow(self):
        self.window = Model(self.conn)
        self.window.show()

    def goToProducersWindow(self):
        self.window = Producent(self.conn)
        self.window.show()

    def goToStopsWindow(self):
        self.window = Stop(self.conn)
        self.window.show()

    def goToTicketWindow(self):
        self.window = Tickets(self.conn)
        self.window.show()

    def goToTicketOfficeWindow(self):
        self.window = TicketOffice(self.conn)
        self.window.show()

    def goToTicketMachineWindow(self):
        self.window = TicketMachine(self.conn)
        self.window.show()

    def goToVehiclesWindow(self):
        self.window = Vehicle(self.conn)
        self.window.show()

    def goToWhereWindow(self):
        self.window = Where(self.conn)
        self.window.show()

    def goToZonesWindow(self):
        self.window = Zone(self.conn)
        self.window.show()
