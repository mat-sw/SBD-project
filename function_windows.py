from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox
from FunctionWindow import FunctionWindow
import sys
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
    cur.execute("DELETE FROM %s WHERE %s = '" % (db, what) + item + "';")
    conn.commit()
    cur.close()


def select_from_db(table, conn):
    cur = conn.cursor()
    cur.execute("Select * from %s ORDER By 1;" % table)
    data = cur.fetchall()
    cur.close()
    return data


class Przyjazdy(FunctionWindow):
    def __init__(self, conn):
        super(Przyjazdy, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Przyjazdy")


class Bilety(FunctionWindow):
    def __init__(self, conn):
        super(Bilety, self).__init__()
        self.initialze_grid()

        self.setup(pos + 50, size, "Bilety")


class Miasta(FunctionWindow):
    def __init__(self, conn):
        super(Miasta, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Nazwa", "Status", "Liczba mieszkańców", "Powierzchnia", "Gęstość"]
        self.data = select_from_db("miasta", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([item[0], item[1], str(item[2]), str(item[3]), str(round(item[4], 2)), "Usuń"]):
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(len(self.labels)):
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Miasta")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("miasta", "nazwa_miasta", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO miasta (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) "
                        "VALUES('" + item(row, 0).text() + "', '" + item(row, 1).text() + "', " + item(row, 2).text() + ", " + item(row, 3).text() + ");")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Pojazdy(FunctionWindow):
    def __init__(self, conn):
        super(Pojazdy, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Pojazdy")


class Kierowcy(FunctionWindow):
    def __init__(self, conn):
        super(Kierowcy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Pesel", "Imie", "Nazwisko", "Płeć", "Czy prowadzi autbous", "Czy prowadzi tramwaj", "Wynagrodzenie", "Data zatrudnienia", "Stan_cywilny"]
        self.data = select_from_db("kierowcy", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([item[0], item[1], item[2], item[3], item[4], item[5], str(item[6]), str(item[7]), item[8], "Usuń"]):
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(len(self.labels)):
            if i == 3:
                lista_plec = QComboBox(self)
                lista_plec.addItems(["", "mezczyzna", "kobieta"])
                self.view.setCellWidget(self.last_row, i, lista_plec)
                continue
            if i == 4 or i == 5:
                lista_tak_nie = QComboBox(self)
                lista_tak_nie.addItems(["", "tak", "nie"])
                self.view.setCellWidget(self.last_row, i, lista_tak_nie)
                continue
            if i == 8:
                lista_stan = QComboBox(self)
                lista_stan.addItems(['', 'zonaty', 'zamezna', 'wdowiec', 'wdowa', 'panna', 'kawaler', 'rozwiedziony', 'rozwiedziona', 'w separacji'])
                self.view.setCellWidget(self.last_row, i, lista_stan)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Kierowcy")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("kierowcy", "pesel", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            print("Dodaj funckjonalnosc")
            cur = self.conn.cursor()
            # cur.execute("INSERT INTO kierowcy VALUES("+ item(self.last_row, 0).text() +", '"+ item(self.last_row, 1).text() +"');" )
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Modele(FunctionWindow):
    def __init__(self, conn):
        super(Modele, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Modelu", "Nazwa Modelu", "Typ pojazdu", "Czy niskopodłogowy", "Miejsca siedzące", "Miejsca stojące", "ID producenta"]
        self.data = select_from_db("modele_pojazdow", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], item[2], item[3], str(item[4]), str(item[5]), str(item[6]), "Usuń"]):
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, len(self.labels)):
            if i == 2:
                lista_typ = QComboBox(self)
                lista_typ.addItems(["", "tramwaj", "autobus"])
                self.view.setCellWidget(self.last_row, i, lista_typ)
                continue
            if i == 3:
                lista_tak_nie = QComboBox(self)
                lista_tak_nie.addItems(["", "tak", "nie"])
                self.view.setCellWidget(self.last_row, i, lista_tak_nie)
                continue
            if i == 6:
                lista_prod = QComboBox(self)
                cur = conn.cursor()
                cur.execute("SELECT id_producenta FROM producenci")
                ids = cur.fetchall()
                cur.close()
                lista_prod.addItem("")
                for item in ids:
                    lista_prod.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista_prod)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Modele")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("modele_pojazdow", "id_modelu", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO modele_pojazdow VALUES(NEXTVAL('model_seq'), '" + item(row, 1).text() + "', '" + item(row, 2).currentText() + "', '" +
                        item(row, 3).currentText() + "', " + item(row, 4).text() + ", " + item(row, 5).text() + ", " + item(row, 6).currentText() + ");")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Producenci(FunctionWindow):
    def __init__(self, conn):
        super(Producenci, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID producenta", "Nazwa"]
        self.data = select_from_db("producenci", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], "Usuń"]):
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(len(self.labels)):
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Producenci")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("producenci", "id_producenta", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO producenci VALUES(NEXTVAL('producer_seq'), '" + item(row, 1).text() + "');")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Kasy(FunctionWindow):
    def __init__(self, conn):
        super(Kasy, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Kasy biletowe")


class Linie(FunctionWindow):
    def __init__(self, conn):
        super(Linie, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID linii", "Typ linii"]
        self.data = select_from_db("linie", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(item[0])))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem("Usuń"))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        self.view.setCellWidget(self.last_row, 0, QLineEdit())
        lista_linia = QComboBox(self)
        lista_linia.addItems(["", "autobusowa", "tramwajowa"])
        self.view.setCellWidget(self.last_row, 1, lista_linia)

        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Linie")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("linie", "id_linii", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO linie VALUES(" + item(row, 0).text() + ", '" + item(row, 1).currentText() + "');")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Przystanki(FunctionWindow):
    def __init__(self, conn):
        super(Przystanki, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Przystanki")


class Kolejnosc(FunctionWindow):
    def __init__(self, conn):
        super(Kolejnosc, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "kolejność przystanków")


class Biletomaty(FunctionWindow):
    def __init__(self, conn):
        super(Biletomaty, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Biletomatu", "Płatność gotówką", "Płatność kartą"]
        self.data = select_from_db("biletomaty", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [" "])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(item[0])))
            self.view.setItem(rows, 1, QTableWidgetItem(item[1]))
            self.view.setItem(rows, 2, QTableWidgetItem(item[2]))
            self.view.setItem(rows, 3, QTableWidgetItem("Usuń"))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, 3):
            lista_tak_nie = QComboBox(self)
            lista_tak_nie.addItems(['', 'tak', 'nie'])
            self.view.setCellWidget(self.last_row, i, lista_tak_nie)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Biletomaty")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("biletomaty", "id_biletomatu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO biletomaty VALUES(NEXTVAL('biletomat_seq'), '" + item(row, 1).currentText() + "', '" + item(row, 2).currentText() + "');")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Zone(FunctionWindow):
    def __init__(self, conn):
        super(Zone, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Typ strefy"]
        self.data = select_from_db("strefy", self.conn)
        self.view.setColumnCount(len(self.labels) + 1)
        self.view.setHorizontalHeaderLabels(self.labels + [" "])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(item[0]))
            self.view.setItem(rows, 1, QTableWidgetItem("Usuń"))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        lista_strefy = QComboBox(self)
        lista_strefy.addItems(['', 'A', 'B', 'C', 'AB', 'ABC'])
        self.view.setCellWidget(self.last_row, 0, lista_strefy)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Strefy")

    def fun_del(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("strefy", "typ_strefy", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            cur = self.conn.cursor()
            cur.execute("INSERT INTO strefy VALUES('" + item(self.last_row, 0).currentText() + "');")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Gdzie(FunctionWindow):
    def __init__(self, conn):
        super(Gdzie, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Gdzie można kupić bilet")
