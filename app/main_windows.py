from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
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

        for button in [self.bilet, self.kierowcy_pojazdy, self.biletomat, self.kasa, self.pojazd, self.model,
                       self.producent, self.kierowca, self.linia, self.przystanek, self.strefa, self.miasto, self.przyjazdy, self.kolejnosc]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")
            button.setMinimumSize(QSize(160, 30))

        self.my_grid.addWidget(self.wyloguj, 0, 3, Qt.AlignCenter)
        self.my_grid.addWidget(self.info_label, 1, 0, 1, 4, Qt.AlignHCenter)

        for i, button in enumerate([self.bilet, self.biletomat, self.kasa, self.kierowcy_pojazdy, self.model, self.producent, self.pojazd, self.kierowca,
                                    self.linia, self.przystanek, self.strefa, self.miasto, self.przyjazdy, self.kolejnosc]):
            self.my_grid.addWidget(button, int(i/4) + 2, i % 4, Qt.AlignCenter)

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
        self.kierowcy_pojazdy = QPushButton("Kierowcy a pojazdy", self)
        self.przyjazdy = QPushButton("Przyjazdy", self)
        self.kolejnosc = QPushButton("Kolejność przystanków", self)

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

    def choose(self):
        self.bilet.clicked.connect(self.goToTicketWindow)
        self.kierowca.clicked.connect(self.goToDriverWindow)
        self.kierowcy_pojazdy.clicked.connect(self.goToDVWindow)
        self.biletomat.clicked.connect(self.goToTicketMachineWindow)
        self.kasa.clicked.connect(self.goToTicketOfficeWindow)
        self.pojazd.clicked.connect(self.goToVehiclesWindow)
        self.model.clicked.connect(self.goToModelWindow)
        self.producent.clicked.connect(self.goToProducersWindow)
        self.linia.clicked.connect(self.goToLinesWindow)
        self.przystanek.clicked.connect(self.goToStopsWindow)
        self.strefa.clicked.connect(self.goToZonesWindow)
        self.miasto.clicked.connect(self.goToCityWindow)
        self.przyjazdy.clicked.connect(self.goToArrivalWindow)
        self.kolejnosc.clicked.connect(self.goToStopOrderWindow)
        self.wyloguj.clicked.connect(self.goToLoginWindow)

    def goToLoginWindow(self):
        self.window = LoginWindow()
        self.close()
        self.window.show()

    def goToCityWindow(self):
        self.window = Miasta(self.conn)
        self.window.show()

    def goToDriverWindow(self):
        self.window = Kierowcy(self.conn)
        self.window.show()

    def goToLinesWindow(self):
        self.window = Linie(self.conn)
        self.window.show()

    def goToModelWindow(self):
        self.window = Modele(self.conn)
        self.window.show()

    def goToProducersWindow(self):
        self.window = Producenci(self.conn)
        self.window.show()

    def goToStopsWindow(self):
        self.window = Przystanki(self.conn)
        self.window.show()

    def goToTicketWindow(self):
        self.window = Bilety(self.conn)
        self.window.show()

    def goToTicketOfficeWindow(self):
        self.window = Kasy(self.conn)
        self.window.show()

    def goToTicketMachineWindow(self):
        self.window = Biletomaty(self.conn)
        self.window.show()

    def goToVehiclesWindow(self):
        self.window = Pojazdy(self.conn)
        self.window.show()

    def goToDVWindow(self):
        self.window = KierowcyPojazdy(self.conn)
        self.window.show()

    def goToZonesWindow(self):
        self.window = Strefy(self.conn)
        self.window.show()

    def goToArrivalWindow(self):
        self.window = Przyjazdy(self.conn)
        self.window.show()

    def goToStopOrderWindow(self):
        self.window = Kolejnosc(self.conn)
        self.window.show()
