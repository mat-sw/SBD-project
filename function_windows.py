from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget,\
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from WindowInterface import WindowInterface
from FunctionWindow import FunctionWindow
import numpy as np


width = 1000
height = 600
pos = np.array([1920 / 2 - width / 2, 1080 / 2 - height / 2])
size = np.array([width, height])

class Tickets(QWidget):
    def __init__(self):
        super(Tickets, self).__init__()
        self.main_grid = QVBoxLayout()
        # self.add = QPushButton("Dodaj", self)
        # self.delete = QPushButton("Usuń dane", self)
        # self.modify = QPushButton("Modyfikuj dane", self)
        # self.show = QPushButton("Wyświetl dane", self)
        self.setup(pos, size, "Tickets")

    def add_buttons(self):
        self.add = QPushButton("Dodaj", self)
        self.delete = QPushButton("Usuń dane", self)
        self.modify = QPushButton("Modyfikuj dane", self)
        self.show = QPushButton("Wyświetl dane", self)

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)

    def initialze_grid(self):
        self.main_grid = QVBoxLayout()
        self.add_buttons()
        for button in [self.add, self.delete, self.modify, self.show]:
            button.setStyleSheet("background-color: rgb(171, 195, 249); font-size : 9pt")
        self.main_grid.addWidget(self.add, 0, 0)
        self.main_grid.addWidget(self.delete, 0, 1)
        self.main_grid.addWidget(self.modify, 1, 0)
        self.main_grid.addWidget(self.show, 1, 1)


class City(FunctionWindow):
    def __init__(self, pos, size):
        super(City, self).__init__()
        # self.initialze_grid()
        self.setup(pos, size, "Cities")


class Vehicle(WindowInterface):
    def __init__(self, pos, size):
        super(Vehicle, self).__init__()
        self.setup(pos, size, "Vehicles")


class Driver(WindowInterface):
    def __init__(self, pos, size):
        super(Driver, self).__init__()
        self.setup(pos, size, "Drivers")


class Model(WindowInterface):
    def __init__(self, pos, size):
        super(Model, self).__init__()
        self.setup(pos, size, "Models")


class Producent(WindowInterface):
    def __init__(self, pos, size):
        super(Producent, self).__init__()
        self.setup(pos, size, "Producers")


class TicketOffice(WindowInterface):
    def __init__(self, pos, size):
        super(TicketOffice, self).__init__()
        self.setup(pos, size, "Ticket Offices")


class Line(WindowInterface):
    def __init__(self, pos, size):
        super(Line, self).__init__()
        self.setup(pos, size, "Lines")


class Stop(WindowInterface):
    def __init__(self, pos, size):
        super(Stop, self).__init__()
        self.setup(pos, size, "Stops")


class TicketMachine(WindowInterface):
    def __init__(self, pos, size):
        super(TicketMachine, self).__init__()
        self.setup(pos, size, "Ticket Machines")


class Zone(WindowInterface):
    def __init__(self, pos, size):
        super(Zone, self).__init__()
        self.setup(pos, size, "Zones")


class Where(WindowInterface):
    def __init__(self, pos, size):
        super(Where, self).__init__()
        self.setup(pos, size, "Where")
