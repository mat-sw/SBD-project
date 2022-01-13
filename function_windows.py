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


def select_from_db(what, table, conn):
    cur = conn.cursor()
    cur.execute("Select %s from %s ORDER By 1;" % (what, table))
    data = cur.fetchall()
    cur.close()
    return data


def remove_duplicates(x):
    return list(dict.fromkeys(x))


class Przyjazdy(FunctionWindow):
    def __init__(self, conn):
        super(Przyjazdy, self).__init__()
        self.initialze_grid()
        self.setup(pos + 50, size, "Przyjazdy")


class Bilety(FunctionWindow):
    def __init__(self, conn):
        super(Bilety, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Biletu", "Czy ulgowy?", "Cena", "Czas przejazdu", "Strefa"]
        self.data = select_from_db("*", "bilety", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + [" ", " "])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], str(item[2]), item[3], item[4], "Modyfikuj", "Usuń"]):
                if i == 1:
                    lista_tak_nie = QComboBox(self)
                    lista_tak_nie.addItem(item[i])
                    for id in ['tak', 'nie']:
                        if id != item[i]:
                            lista_tak_nie.addItem(id)
                    self.view.setCellWidget(rows, i, lista_tak_nie)
                    continue
                if i == 3:
                    lista_czas = QComboBox(self)
                    lista_czas.addItem(item[i])
                    for id in ['15', '30', '60']:
                        if id != item[i]:
                            lista_czas.addItem(id)
                    self.view.setCellWidget(rows, i, lista_czas)
                    continue
                if i == 4:
                    lista_stref = QComboBox(self)
                    lista_stref.addItem(item[i])
                    for id in ['A', 'B', 'C', 'AB', 'ABC']:
                        if id != item[i]:
                            lista_stref.addItem(id)
                    self.view.setCellWidget(rows, i, lista_stref)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        lista_tak_nie = QComboBox(self)
        lista_tak_nie.addItems(['', 'tak', 'nie'])
        self.view.setCellWidget(self.last_row, 1, lista_tak_nie)
        lista_czas = QComboBox(self)
        lista_czas.addItems(['', '15', '30', '60'])
        self.view.setCellWidget(self.last_row, 3, lista_czas)
        lista_strefy = QComboBox(self)
        lista_strefy.addItems(['', 'A', 'B', 'C', 'AB', 'ABC'])
        self.view.setCellWidget(self.last_row, 4, lista_strefy)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Bilety")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("bilety", "id_biletu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE bilety SET id_biletu = " + self.view.item(item.row(), 0).text() + ", czy_ulgowy = '" + self.view.cellWidget(item.row(), 1).currentText() + "', cena = " + self.view.item(item.row(), 2).text() + ", "
                             "czas_przejazdu = '" + self.view.cellWidget(item.row(), 3).currentText() + "', strefa_typ_strefy = '" + self.view.cellWidget(item.row(), 4).currentText() + "' WHERE id_biletu = " + str(self.data[item.row()][0]) + ";")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO bilety VALUES(NEXTVAL('bilet_seq'), '" + item(row, 1).currentText() + "', 0, '" + item(row, 3).currentText() + "', '" + item(row, 4).currentText() + "');")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Miasta(FunctionWindow):
    def __init__(self, conn):
        super(Miasta, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Nazwa", "Status", "Liczba mieszkańców", "Powierzchnia", "Gęstość zaludnienia"]
        self.data = select_from_db("*", "miasta", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([item[0], item[1], str(item[2]), str(item[3]), str(round(item[4], 2)), "Modyfikuj", "Usuń"]):
                if i == 1:
                    lista_status = QComboBox(self)
                    lista_status.addItem(item[i])
                    for id in ["miasto", "wies"]:
                        if id != item[i]:
                            lista_status.addItem(id)
                    self.view.setCellWidget(rows, i, lista_status)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(len(self.labels)-1):
            if i == 1:
                lista_status = QComboBox(self)
                lista_status.addItems(["", "miasto", "wies"])
                self.view.setCellWidget(self.last_row, i, lista_status)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Miasta")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("miasta", "nazwa_miasta", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE miasta SET nazwa_miasta = '" + self.view.item(item.row(), 0).text() + "', status = '" + self.view.cellWidget(item.row(), 1).currentText() + "', liczba_mieszkancow = " + self.view.item(item.row(), 2).text() + ", "
                             "powierzchnia = " + self.view.item(item.row(), 3).text() + ", gestosc_zaludnienia = " + self.view.item(item.row(), 4).text() + " WHERE nazwa_miasta = '" + self.data[item.row()][0] + "';")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO miasta (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) "
                        "VALUES('" + item(row, 0).text() + "', '" + item(row, 1).currentText() + "', " + item(row, 2).text() + ", " + item(row, 3).text() + ");")
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

        self.conn = conn
        self.labels = ["ID pojazdu", "Max liczba osob", "ID Linii", "ID biletomatu", "Rok produkcji", "Data waznosci przegladu", "ID modelu", "ID producenta"]
        self.data = select_from_db("*", "pojazdy", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]), str(item[7]), "Modyfikuj", "Usuń"]):
                if i == 2:
                    lista_linii = QComboBox(self)
                    lista_linii.addItem(str(item[i]))
                    ids = select_from_db("id_linii", "linie", conn)
                    for id in ids:
                        if id[0] != item[i]:
                            lista_linii.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_linii)
                    continue
                if i == 3:
                    lista_bil = QComboBox(self)
                    if str(item[i]) == "None":
                        lista_bil.addItem('-')
                    else:
                        lista_bil.addItem(str(item[i]))
                    ids = select_from_db("id_biletomatu", "biletomaty", conn)
                    for id in ids:
                        if id[0] != item[i]:
                            lista_bil.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_bil)
                    continue
                if i == 6:
                    lista = QComboBox(self)
                    lista.addItem(str(item[i]))
                    ids = select_from_db("id_modelu", "modele_pojazdow", conn)
                    for id in ids:
                        if id[0] != item[i]:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(2, len(self.labels)-1):
            if i == 2:
                lista = QComboBox(self)
                ids = select_from_db("id_linii", "linie", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 3:
                lista = QComboBox(self)
                ids = select_from_db("id_biletomatu", "biletomaty", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 6:
                lista = QComboBox(self)
                ids = select_from_db("id_modelu", "modele_pojazdow", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Pojazdy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("pojazdy", "id_pojazdu", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                bil = self.view.cellWidget(item.row(), 3).currentText()
                if bil == "None":
                    bil = "null"
                cur = self.conn.cursor()
                cur.execute("UPDATE pojazdy SET id_pojazdu = " + self.view.item(item.row(), 0).text() + ", max_liczba_osob = (SELECT sum_sits("+ self.view.cellWidget(item.row(), 6).currentText() + ")), "
                            "linie_id_linii = " + self.view.cellWidget(item.row(), 2).currentText() + ", biletomaty_id_biletomatu = " + bil + ", rok_produkcji = " + self.view.item(item.row(), 4).text() +
                            ", data_waznosci_przegladu = to_date('" + self.view.item(item.row(), 5).text() + "', 'YYYY-MM-DD'), modele_poj_id_modelu = " + self.view.cellWidget(item.row(), 6).currentText() +
                            ", modele_poj_prod_id_producenta = " + self.view.item(item.row(), 7).text() + " WHERE id_pojazdu = " + str(self.data[item.row()][0]) + ";")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            bil = item(row, 3).currentText()
            if bil == "":
                bil = "null"
            cur.execute("INSERT INTO pojazdy VALUES(NEXTVAL('pojazd_seq'), (SELECT sum_sits("+ item(row, 6).currentText() + ")), "+ item(row, 2).currentText() +", "+ bil +", "+ item(row, 4).text() +
                        ", to_date('"+ item(row, 5).text() +"', 'YYYY-MM-DD'), "+ item(row, 6).currentText() +", (SELECT producenci_id_producenta FROM modele_pojazdow WHERE id_modelu = "+ item(row, 6).currentText() +"));" )
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


class Kierowcy(FunctionWindow):
    def __init__(self, conn):
        super(Kierowcy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Pesel", "Imie", "Nazwisko", "Płeć", "Czy prowadzi autbous", "Czy prowadzi tramwaj", "Wynagrodzenie", "Data zatrudnienia", "Stan_cywilny"]
        self.data = select_from_db("*", "kierowcy", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([item[0], item[1], item[2], item[3], item[4], item[5], str(item[6]), str(item[7]), item[8], "Modyfikuj", "Usuń"]):
                if i == 3:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ["mezczyzna", "kobieta"]:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 4 or i == 5:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ["tak", "nie"]:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 8:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ['zonaty', 'zamezna', 'wdowiec', 'wdowa', 'panna', 'kawaler', 'rozwiedziony', 'rozwiedziona', 'w separacji']:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(len(self.labels)):
            if i == 3:
                lista = QComboBox(self)
                lista.addItems(["", "mezczyzna", "kobieta"])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 4 or i == 5:
                lista = QComboBox(self)
                lista.addItems(["", "tak", "nie"])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 8:
                lista = QComboBox(self)
                lista.addItems(['', 'zonaty', 'zamezna', 'wdowiec', 'wdowa', 'panna', 'kawaler', 'rozwiedziony', 'rozwiedziona', 'w separacji'])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Kierowcy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("kierowcy", "pesel", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE kierowcy SET pesel = '" + self.view.item(item.row(), 0).text() + "', imie = '" + self.view.item(item.row(), 1).text() + "', nazwisko = '" + self.view.item(item.row(), 2).text() + "', "
                            "plec = '" + self.view.cellWidget(item.row(), 3).currentText() + "', uprawnienia_autobusowe = '" + self.view.cellWidget(item.row(), 4).currentText() + "'"
                            ", uprawnienia_tramwajowe = '" + self.view.cellWidget(item.row(), 5).currentText() + "', placa = " + self.view.item(item.row(), 6).text() +
                            ", data_zatrudnienia = to_date('" + self.view.item(item.row(), 7).text() + "', 'YYYY-MM-DD'), stan_cywilny = '" + self.view.cellWidget(item.row(), 8).currentText() + "' WHERE pesel = '" + self.data[item.row()][0] + "';")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("INSERT INTO kierowcy VALUES('"+ item(row, 0).text() +"', '"+ item(row, 1).text() +"', '"+ item(row, 2).text() +"', '"+ item(row, 3).currentText() +"' ,'"+ item(row, 4).currentText() +
                        "', '"+ item(row, 5).currentText() +"', "+ item(row, 6).text() +", to_date('"+ item(row, 7).text() +"', 'YYYY-MM-DD'), '"+ item(row, 8).currentText() +"');" )
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
        self.data = select_from_db("*", "modele_pojazdow", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], item[2], item[3], str(item[4]), str(item[5]), str(item[6]), "Modyfikuj", "Usuń"]):
                if i == 2:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ["tramwaj", "autobus"]:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 3:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ["tak", "nie"]:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 6:
                    lista = QComboBox(self)
                    lista.addItem(str(item[i]))
                    ids = select_from_db("id_producenta", "producenci", conn)
                    for id in ids:
                        if id[0] != item[i]:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, len(self.labels)):
            if i == 2:
                lista = QComboBox(self)
                lista.addItems(["", "tramwaj", "autobus"])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 3:
                lista = QComboBox(self)
                lista.addItems(["", "tak", "nie"])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 6:
                lista = QComboBox(self)
                ids = select_from_db("id_producenta", "producenci", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Modele")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("modele_pojazdow", "id_modelu", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE modele_pojazdow SET id_modelu = " + self.view.item(item.row(), 0).text() + ", nazwa_modelu = '" + self.view.item(item.row(), 1).text() + "', typ_pojazdu = '" + self.view.cellWidget(item.row(), 2).currentText() + "', "
                            "czy_niskopodlogowy = '" + self.view.cellWidget(item.row(), 3).currentText() + "', liczba_miejsc_siedzacych = " + self.view.item(item.row(), 4).text() + ", "
                            "liczba_miejsc_stojacych = " + self.view.item(item.row(), 5).text() + ", producenci_id_producenta = " + self.view.cellWidget(item.row(), 6).currentText() + " WHERE id_modelu = '" + str(self.data[item.row()][0]) + "';")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
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
        self.data = select_from_db("*", "producenci", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], "Modyfikuj", "Usuń"]):
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, len(self.labels)):
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Producenci")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("producenci", "id_producenta", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE producenci SET id_producenta = " + self.view.item(item.row(), 0).text() + ", nazwa_producenta = '" + self.view.item(item.row(), 1).text() + "' WHERE id_producenta = " + str(self.data[item.row()][0]) + ";")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
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
        self.data = select_from_db("*", "linie", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], "Modyfikuj", "Usuń"]):
                if i == 1:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ["autobusowa", "tramwajowa"]:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        self.view.setCellWidget(self.last_row, 0, QLineEdit())
        lista = QComboBox(self)
        lista.addItems(["", "autobusowa", "tramwajowa"])
        self.view.setCellWidget(self.last_row, 1, lista)

        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, size, "Linie")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("linie", "id_linii", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE linie SET id_linii = " + self.view.item(item.row(), 0).text() + ", typ_linii = '" + self.view.cellWidget(item.row(), 1).currentText() + "' WHERE id_linii = " + str(self.data[item.row()][0]) + ";")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
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
        self.data = select_from_db("*", "biletomaty", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["",""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], item[2], "Modyfikuj", "Usuń"]):
                if i in [1, 2]:
                    lista = QComboBox(self)
                    lista.addItem(item[i])
                    for id in ['tak', 'nie']:
                        if id != item[i]:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, 3):
            lista = QComboBox(self)
            lista.addItems(['', 'tak', 'nie'])
            self.view.setCellWidget(self.last_row, i, lista)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Biletomaty")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("biletomaty", "id_biletomatu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE biletomaty SET id_biletomatu = " + self.view.item(item.row(), 0).text() + ", platnosc_gotowka = '" + self.view.cellWidget(item.row(), 1).currentText() + "'"
                            ", platnosc_karta = '" + self.view.cellWidget(item.row(), 2).currentText() + "' WHERE id_biletomatu = " + str(self.data[item.row()][0]) + ";")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
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
        self.data = select_from_db("*", "strefy", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            lista = QComboBox(self)
            lista.addItem(item[0])
            for id in ['A', 'B', 'C', 'AB', 'ABC']:
                if id != item[0]:
                    lista.addItem(id)
            self.view.setCellWidget(rows, 0, lista)
            self.view.setItem(rows, 1, QTableWidgetItem("Modyfikuj"))
            self.view.setItem(rows, 2, QTableWidgetItem("Usuń"))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        lista = QComboBox(self)
        lista.addItems(['', 'A', 'B', 'C', 'AB', 'ABC'])
        self.view.setCellWidget(self.last_row, 0, lista)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Strefy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("strefy", "typ_strefy", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE strefy SET typ_strefy = '" + self.view.item(item.row(), 0).text() + "' WHERE typ_strefy = '" + self.data[item.row()][0] + "';")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
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


class KierowcyPojazdy(FunctionWindow):
    def __init__(self, conn):
        super(KierowcyPojazdy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Pojazdu", "ID Linii", "ID Modelu", "ID producenta", "Pesel kierowcy"]
        self.data = select_from_db("*", "kierowcy_i_pojazdy", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), str(item[3]), item[4], "Modyfikuj", "Usuń"]):
                if i == 0:
                    lista_pojazdy = QComboBox(self)
                    ids = select_from_db("id_pojazdu", "pojazdy", conn)
                    lista_pojazdy.addItem(str(item[0]))
                    for id in ids:
                        if id[0] != item[0]:
                            lista_pojazdy.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_pojazdy)
                    continue
                if i == 4:
                    lista_pesele = QComboBox(self)
                    pesele = select_from_db("pesel", "kierowcy", conn)
                    lista_pesele.addItem(item[4])
                    for id in pesele:
                        if id[0] != item[4]:
                            lista_pesele.addItem(id[0])
                    self.view.setCellWidget(rows, i, lista_pesele)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        lista_pojazdy = QComboBox(self)
        ids = select_from_db("id_pojazdu", "pojazdy", conn)
        lista_pojazdy.addItem("")
        for item in ids:
            lista_pojazdy.addItem(str(item[0]))
        self.view.setCellWidget(self.last_row, 0, lista_pojazdy)

        lista_pesele = QComboBox(self)
        pesele = select_from_db("pesel", "kierowcy", conn)
        lista_pesele.addItem("")
        for item in pesele:
            lista_pesele.addItem(item[0])
        self.view.setCellWidget(self.last_row, 4, lista_pesele)

        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, size, "Kierowcy a pojazdy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("strefy", "typ_strefy", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                id_pojazdu = self.view.cellWidget(item.row(), 0).currentText()
                cur.execute("UPDATE kierowcy_i_pojazdy SET pojazdy_id_pojazdu = " + id_pojazdu + ", pojazdy_linie_id_linii = (SELECT linie_id_linii FROM pojazdy WHERE id_pojazdu = " + id_pojazdu +
                            "), pojazdy_id_modelu = (SELECT modele_poj_id_modelu FROM pojazdy WHERE id_pojazdu = " + id_pojazdu + "), "
                            "pojazdy_id_producenta = (SELECT modele_poj_prod_id_producenta FROM pojazdy WHERE id_pojazdu = " + id_pojazdu + "), "
                            "kierowcy_pesel = '" + self.view.cellWidget(item.row(), 4).currentText() + "' WHERE pojazdy_id_pojazdu = " + str(self.data[item.row()][0]) +
                            " AND kierowcy_pesel = '" + self.data[item.row()][4] + "';")
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            cur = self.conn.cursor()
            cur.execute("INSERT INTO kierowcy_i_pojazdy VALUES(" + item(self.last_row, 0).currentText() + ", (SELECT linie_id_linii FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), "
                        "(SELECT modele_poj_id_modelu FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), "
                        "(SELECT modele_poj_prod_id_producenta FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), "+ item(self.last_row, 4).currentText() + ");")
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
