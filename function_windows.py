from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class Tickets(QWidget):
    def __init__(self, pos, size):
        super(Tickets, self).__init__()
        self.setup(pos, size, "Tickets")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class City(QWidget):
    def __init__(self, pos, size):
        super(City, self).__init__()
        self.setup(pos, size, "Cities")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Vehicle(QWidget):
    def __init__(self, pos, size):
        super(Vehicle, self).__init__()
        self.setup(pos, size, "Vehicles")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Driver(QWidget):
    def __init__(self, pos, size):
        super(Driver, self).__init__()
        self.setup(pos, size, "Drivers")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Model(QWidget):
    def __init__(self, pos, size):
        super(Model, self).__init__()
        self.setup(pos, size, "Models")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Producent(QWidget):
    def __init__(self, pos, size):
        super(Producent, self).__init__()
        self.setup(pos, size, "Producers")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class TicketOffice(QWidget):
    def __init__(self, pos, size):
        super(TicketOffice, self).__init__()
        self.setup(pos, size, "Ticket Offices")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Line(QWidget):
    def __init__(self, pos, size):
        super(Line, self).__init__()
        self.setup(pos, size, "Lines")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Stop(QWidget):
    def __init__(self, pos, size):
        super(Stop, self).__init__()
        self.setup(pos, size, "Stops")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class TicketMachine(QWidget):
    def __init__(self, pos, size):
        super(TicketMachine, self).__init__()
        self.setup(pos, size, "Ticket Machines")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Zone(QWidget):
    def __init__(self, pos, size):
        super(Zone, self).__init__()
        self.setup(pos, size, "Zones")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)


class Where(QWidget):
    def __init__(self, pos, size):
        super(Where, self).__init__()
        self.setup(pos, size, "Where")

    def setup(self, pos, size, title):
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setWindowTitle(title)
