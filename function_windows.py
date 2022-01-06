from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtGui import QIcon
from FunctionWindow import FunctionWindow
import sys
import numpy as np
import psycopg2
import pandas as pd

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
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def delete_from_db(db, what, item, conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM %s WHERE %s = '" % (db, what) + item +"';")
    conn.commit()
    cur.close()


def select_from_db(table, conn):
    cur = conn.cursor()
    cur.execute("Select * from %s;" % table)
    data = cur.fetchall()
    cur.close()
    return data


class Arrival(FunctionWindow):
    def __init__(self, conn):
        super(Arrival, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Przyjazdy")


class Tickets(FunctionWindow):
    def __init__(self, conn):
        super(Tickets, self).__init__()
        self.initialze_grid()

        self.view.setColumnCount(2)
        self.view.setHorizontalHeaderLabels(["ID biletu", "Ulgowy?"])
        query = QSqlQuery()
        query.exec("""SELECT id_typu_biletu, czy_ulgowy from bilet""")

        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
        self.view.resizeColumnsToContents()

        self.setup(pos, size / 2, "Bilety")


class City(FunctionWindow):
    def __init__(self, conn):
        super(City, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Nazwa", "Status", "Liczba mieszkańców", "Powierzchnia"]
        self.data = select_from_db("miasto", self.conn)
        self.view.setColumnCount(len(self.labels)+1)
        self.view.setHorizontalHeaderLabels(self.labels+[""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(item[0]))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem(str(item[2])))
            self.view.setItem(rows, 3, QTableWidgetItem(str(item[3])))
            self.view.setItem(rows, 4, QTableWidgetItem("Usuń"))
        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos, size / 2, "Miasta")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("miasto", "nazwa_miasta",  self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")


class Vehicle(FunctionWindow):
    def __init__(self, conn):
        super(Vehicle, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Pojazdy")


class Driver(FunctionWindow):
    def __init__(self, conn):
        super(Driver, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Kierowcy")


class Model(FunctionWindow):
    def __init__(self, conn):
        super(Model, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Modele")


class Producent(FunctionWindow):
    def __init__(self, conn):
        super(Producent, self).__init__()
        self.initialze_grid()
        # self.main_grid = QGridLayout()
        # self.model = QSqlTableModel(self)
        # self.model.setTable("producent")
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # self.model.setHeaderData(0, Qt.Horizontal, "id_producenta")
        # self.model.setHeaderData(1, Qt.Horizontal, "nazwa_producenta")
        # self.model.select()
        # # Set up the view
        # self.view = QTableView()
        # self.view.setModel(self.model)
        # self.view.resizeColumnsToContents()

        self.conn = conn
        self.labels = ["ID producenta", "Nazwa"]
        self.data = select_from_db("producent", self.conn)
        self.view.setColumnCount(len(self.labels)+1)
        self.view.setHorizontalHeaderLabels(self.labels+[""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(item[0])))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem("Usuń"))
        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos, size / 2, "Producenci")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("producent", "id_producenta", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")


class TicketOffice(FunctionWindow):
    def __init__(self, conn):
        super(TicketOffice, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Kasy biletowe")


class Line(FunctionWindow):
    def __init__(self, conn):
        super(Line, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Linie")


class Stop(FunctionWindow):
    def __init__(self, conn):
        super(Stop, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Przystanki")


class StopsOrder(FunctionWindow):
    def __init__(self, conn):
        super(StopsOrder, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "kolejność przystanków")


class TicketMachine(FunctionWindow):
    def __init__(self, conn):
        super(TicketMachine, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Biletomaty")


class TimeOfRide(FunctionWindow):
    def __init__(self, conn):
        super(TimeOfRide, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Czasy przejazdów")


class Zone(FunctionWindow):
    def __init__(self, conn):
        super(Zone, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Typ strefy"]
        self.data = select_from_db("strefa", self.conn)
        self.view.setColumnCount(len(self.labels)+1)
        self.view.setHorizontalHeaderLabels(self.labels+[" "])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(item[0]))
            self.view.setItem(rows, 1, QTableWidgetItem("Usuń"))
        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos, size / 2, "Strefy")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("strefa", "typ_strefy",  self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")


class Where(FunctionWindow):
    def __init__(self, conn):
        super(Where, self).__init__()
        self.initialze_grid()
        self.setup(pos, size / 2, "Gdzie można kupić bilet")
