from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget,\
    QHBoxLayout, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from FunctionWindow import FunctionWindow
import numpy as np
import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "KomunikacjaMiejska"
DB_USER = "postgres"
DB_PASS = "postgres"
width = 1000
height = 600
pos = np.array([1920 / 2 - width / 2, 1080 / 2 - height / 2])
size = np.array([width, height])

def connect_db():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    return conn
    # con = QSqlDatabase.addDatabase("QPSQL")
    # con.setDatabaseName(DB_NAME)
    # con.setHostName(DB_HOST)
    # con.setUserName(DB_USER)
    # con.setPort(DB_PORT)
    # con.setPassword(DB_PASS)
    # if not con.open():
    #     print("dupa")
    #     QMessageBox.critical(
    #         None,
    #         "QTableView Example - Error!",
    #         "Database Error: %s" % con.lastError().databaseText(),
    #         )
    #     return False
    # return True


class Tickets(FunctionWindow):
    def __init__(self, conn):
        super(Tickets, self).__init__()
        self.initialze_grid()

        # cur = conn.cursor()
        # cur.execute("Select id_typu_biletu, czy_ulgowy from bilet")
        self.view.setColumnCount(2)
        self.view.setHorizontalHeaderLabels(["id_biletu", "czy_ulgowy"])
        query = QSqlQuery()
        query.exec("""Select id_typu_biletu, czy_ulgowy from bilet""")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
        self.view.resizeColumnsToContents()
        self.setLayout(self.main_grid)
        self.setup(pos, size/2, "Bilety")


class City(FunctionWindow):
    def __init__(self, conn):
        super(City, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Miasta")


class Vehicle(FunctionWindow):
    def __init__(self, conn):
        super(Vehicle, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Pojazdy")


class Driver(FunctionWindow):
    def __init__(self, conn):
        super(Driver, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Kierowcy")


class Model(FunctionWindow):
    def __init__(self, conn):
        super(Model, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Modele")


class Producent(FunctionWindow):
    def __init__(self, conn):
        super(Producent, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Producenci")


class TicketOffice(FunctionWindow):
    def __init__(self, conn):
        super(TicketOffice, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Kasy biletowe")


class Line(FunctionWindow):
    def __init__(self, conn):
        super(Line, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Linie")


class Stop(FunctionWindow):
    def __init__(self, conn):
        super(Stop, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Przystanki")


class TicketMachine(FunctionWindow):
    def __init__(self, conn):
        super(TicketMachine, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Biletomaty")


class Zone(FunctionWindow):
    def __init__(self, conn):
        super(Zone, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Strefy")


class Where(FunctionWindow):
    def __init__(self, conn):
        super(Where, self).__init__()
        self.initialze_grid()
        self.setup(pos, size/2, "Gdzie można kupić bilet")
