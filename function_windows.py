from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget,\
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from FunctionWindow import FunctionWindow
import numpy as np


width = 1000
height = 600
pos = np.array([1920 / 2 - width / 2, 1080 / 2 - height / 2])
size = np.array([width, height])

class Tickets(FunctionWindow):
    def __init__(self):
        super(Tickets, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Bilety")


class City(FunctionWindow):
    def __init__(self, pos, size):
        super(City, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Miasta")


class Vehicle(FunctionWindow):
    def __init__(self, pos, size):
        super(Vehicle, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Pojazdy")


class Driver(FunctionWindow):
    def __init__(self, pos, size):
        super(Driver, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Kierowcy")


class Model(FunctionWindow):
    def __init__(self, pos, size):
        super(Model, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Modele")


class Producent(FunctionWindow):
    def __init__(self, pos, size):
        super(Producent, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Producenci")


class TicketOffice(FunctionWindow):
    def __init__(self, pos, size):
        super(TicketOffice, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Kasy biletowe")


class Line(FunctionWindow):
    def __init__(self, pos, size):
        super(Line, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Linie")


class Stop(FunctionWindow):
    def __init__(self, pos, size):
        super(Stop, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Przystanki")


class TicketMachine(FunctionWindow):
    def __init__(self, pos, size):
        super(TicketMachine, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Biletomaty")


class Zone(FunctionWindow):
    def __init__(self, pos, size):
        super(Zone, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Strefy")


class Where(FunctionWindow):
    def __init__(self, pos, size):
        super(Where, self).__init__()
        self.initialze_grid()
        self.setup(pos, size, "Gdzie można kupić bilet")
