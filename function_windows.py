from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton, QWidget,\
    QHBoxLayout, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QTableView
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
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
    print(conn)
    return conn
    # do poprawy połączenie bo nie działa xd

    # con = QSqlDatabase.addDatabase("QPSQL")
    # con.setDatabaseName("DB_NAME")
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

def delete_from_db(db, what, item, conn):
    command = "DELETE FROM %s WHERE %s = %s;"
    cur = conn.cursor()
    cur.execute(command, (db, what, item))


class Tickets(FunctionWindow):
    def __init__(self, conn):
        super(Tickets, self).__init__()
        self.initialze_grid()

        # cur = conn.cursor()
        # cur.execute("Select id_typu_biletu, czy_ulgowy from bilet")
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

        self.setup(pos, size/2, "Bilety")


class City(FunctionWindow):
    def __init__(self, conn):
        super(City, self).__init__()
        self.initialze_grid()

        cur = conn.cursor()
        cur.execute("Select * from miasto;")
        data = cur.fetchall()
        self.view.setColumnCount(5)
        self.view.setHorizontalHeaderLabels(["Nazwa", "Status", "Liczba mieszkańców", "Powierzchnia", ""])
        for item in data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(item[0]))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem(str(item[2])))
            self.view.setItem(rows, 3, QTableWidgetItem(str(item[3])))
            self.view.setItem(rows, 4, QTableWidgetItem("Usuń"))
        self.view.resizeColumnsToContents()

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
        cur = self.conn.cursor()
        cur.execute("Select * from producent;")
        self.data = cur.fetchall()
        cur.close()
        self.view.setColumnCount(3)
        self.view.setHorizontalHeaderLabels(["ID producenta", "Nazwa", " "])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(item[0])))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem("Usuń"))
        self.view.resizeColumnsToContents()
        self.get_signal()

        # self.view.setColumnCount(2)
        # self.view.setHorizontalHeaderLabels(["ID producenta", "Nazwa"])
        # query = QSqlQuery()
        # query.exec("""Select * from producent;""")
        # while query.next():
        #     rows = self.view.rowCount()
        #     self.view.setRowCount(rows + 1)
        #     self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
        #     self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
        # self.view.resizeColumnsToContents()
        self.setup(pos, size/2, "Producenci")

    def get_signal(self):
        self.view.clicked.connect(self.func_test)

    def func_test(self, item):
        cellContent = item.data()
        if cellContent == "Usuń":
            cur = self.conn.cursor()
            # print(self.data[item.row()][0])
            cur.execute("DELETE FROM producent WHERE id_producenta = {};".format(self.data[item.row()][0]))
            self.conn.commit()
            cur.close()
            self.close()
        # sf = "You clicked on {}".format(cellContent)
        # print(sf)


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
