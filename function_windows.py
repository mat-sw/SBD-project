from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, \
    QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from WindowInterface import WindowInterface


class Tickets(WindowInterface):
    def __init__(self, pos, size):
        super(Tickets, self).__init__()
        self.setup(pos, size, "Tickets")


class City(WindowInterface):
    def __init__(self, pos, size):
        super(City, self).__init__()
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
