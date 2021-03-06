from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QDateEdit, QTimeEdit
from PyQt5 import QtCore
from FunctionWindow import FunctionWindow
import sys
import numpy as np
import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "KomunikacjaMiejska"
DB_USER = "postgres"
DB_PASS = "postgres"
DATE_FORMAT = 'yyyy-MM-dd'
HOUR_FORMAT = 'hh:mm:ss'
width = 1000
height = 600
pos = np.array([1920 / 2 - width / 2, 1080 / 2 - height / 2])
size = np.array([width, height])

DELETE_ERROR = "Nie można usunąć rekordu. Jest on używany przez inną relację."
UPDATE_ERROR_EXISTS = "Nie można zmienić pola,\nponieważ istnieje już taki klucz unikatowy."
UPDATE_ERROR_VIOLATES = "Nie można zmienić identyfikującego relację atrybutu,\nponieważ jest on używany przez inną relację."
INSERT_ERROR = "Niestety nie można wstawić nowego rekordu.\nSprawdź jeszcze raz dane."


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


def select_from_db(command, conn):
    cur = conn.cursor()
    cur.execute(command)
    data = cur.fetchall()
    cur.close()
    return data


class Biletomaty(FunctionWindow):
    def __init__(self, conn):
        super(Biletomaty, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Biletomatu", "Płatność gotówką", "Płatność kartą"]
        self.data = select_from_db("SELECT * FROM biletomaty ORDER BY 1;", self.conn)
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
        self.setup(pos + 50, [600, height], "Biletomaty")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("biletomaty", "id_biletomatu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE biletomaty SET id_biletomatu = " + self.view.item(item.row(), 0).text() + ", platnosc_gotowka = '" + self.view.cellWidget(item.row(), 1).currentText() + "'" \
                                                                                                                                                                                           ", platnosc_karta = '" + self.view.cellWidget(item.row(), 2).currentText() + "' WHERE id_biletomatu = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO biletomaty VALUES(NEXTVAL('biletomat_seq'), '" + item(row, 1).currentText() + "', '" + item(row, 2).currentText() + "');"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Bilety(FunctionWindow):
    def __init__(self, conn):
        super(Bilety, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Biletu", "Czy ulgowy?", "Cena", "Czas przejazdu", "Strefa"]
        self.data = select_from_db("SELECT * FROM bilety ORDER BY 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
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
        self.view.setCellWidget(self.last_row, 2, QLineEdit())
        lista_czas.addItems(['', '15', '30', '60'])
        self.view.setCellWidget(self.last_row, 3, lista_czas)
        lista_strefy = QComboBox(self)
        lista_strefy.addItems(['', 'A', 'B', 'C', 'AB', 'ABC'])
        self.view.setCellWidget(self.last_row, 4, lista_strefy)
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [700, height], "Bilety")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("bilety", "id_biletu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE bilety SET id_biletu = " + self.view.item(item.row(), 0).text() + ", czy_ulgowy = '" + self.view.cellWidget(item.row(), 1).currentText() + "', cena = " + self.view.item(item.row(), 2).text() + ", "\
                "czas_przejazdu = '" + self.view.cellWidget(item.row(), 3).currentText() + "', strefa_typ_strefy = '" + self.view.cellWidget(item.row(), 4).currentText() + "' WHERE id_biletu = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO bilety VALUES(NEXTVAL('bilet_seq'), '" + item(row, 1).currentText() + "', " + item(row, 2).text() + ", '" + item(row, 3).currentText() + "', '" + item(row, 4).currentText() + "');"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Kasy(FunctionWindow):
    def __init__(self, conn):
        super(Kasy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Kasy", "Godzina otwarca", "Godzina zamknięcia", "Przystanek", "Miasto", "Strefa"]
        self.data = select_from_db("SELECT * FROM kasy_biletowe ORDER BY 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), str(item[3]), item[4], item[5], "Modyfikuj", "Usuń"]):
                if i in [1, 2]:
                    daty = QTimeEdit(self)
                    daty.setCalendarPopup(True)
                    daty.setDisplayFormat(HOUR_FORMAT)
                    daty.setTime(QtCore.QTime(int(_[0:2]), int(_[3:5]), int(_[6:8])))
                    self.view.setCellWidget(rows, i, daty)
                    continue
                if i == 3:
                    nazwa = select_from_db("SELECT nazwa_przystanku FROM przystanki WHERE id_przystanku = " + _ + ";", conn)
                    nazwa = str(nazwa[0])[2:-3]
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT nazwa_przystanku FROM przystanki ORDER BY 1;", conn)
                    lista.addItem(nazwa)
                    for id in ids:
                        if str(id[0]) != nazwa:
                            lista.addItem(id[0])
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        for i in range(1, len(self.labels)-2):
            if i in [1, 2]:
                daty = QTimeEdit(self)
                daty.setCalendarPopup(True)
                daty.setDisplayFormat(HOUR_FORMAT)
                self.view.setCellWidget(self.last_row, i, daty)
                continue
            if i == 3:
                lista = QComboBox(self)
                ids = select_from_db("SELECT nazwa_przystanku FROM przystanki ORDER BY 1;", conn)
                lista.addItem("")
                for id in ids:
                    lista.addItem(str(id[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [800, height], "Kasy biletowe")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                command = "DELETE FROM kasy_biletowe WHERE id_kasy = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                id_przys = self.view.cellWidget(item.row(), 3).currentText()
                command = "UPDATE kasy_biletowe SET id_kasy = " + self.view.item(item.row(), 0).text() + ", godzina_otwarcia = to_timestamp('" + self.view.cellWidget(item.row(), 1).text() + "', 'HH24:MI:SS'), " \
                          "godzina_zamkniecia = to_timestamp('" + self.view.cellWidget(item.row(), 2).text() + "', 'HH24:MI:SS'), przystanki_id_przystanku = (SELECT id_przystanku FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "', "\
                          "przystanki_miasta_nazwa_miasta = (SELECT miasta_nazwa_miasta FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "'), " \
                          "przystanki_strefy_typ_strefy = (SELECT strefy_typ_strefy FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "') WHERE id_kasy = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            command = "INSERT INTO kasy_biletowe VALUES(NEXTVAL('kasa_seq'), to_timestamp('" + item(self.last_row, 1).text() + "', 'HH24:MI:SS'), to_timestamp('" + item(self.last_row, 2).text() + "', 'HH24:MI:SS'), " \
                      "(SELECT id_przystanku FROM przystanki WHERE nazwa_przystanku = '" + item(self.last_row, 3).currentText() + "'), (SELECT miasta_nazwa_miasta FROM przystanki WHERE nazwa_przystanku = '" + item(self.last_row, 3).currentText() + "'), " \
                      "(SELECT strefy_typ_strefy FROM przystanki WHERE nazwa_przystanku = '" + item(self.last_row, 3).currentText() + "'));"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Kierowcy(FunctionWindow):
    def __init__(self, conn):
        super(Kierowcy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Pesel", "Imie", "Nazwisko", "Płeć", "Czy prowadzi autbous", "Czy prowadzi tramwaj", "Wynagrodzenie", "Data zatrudnienia", "Stan_cywilny"]
        self.data = select_from_db("SELECT * FROM kierowcy ORDER BY 3, 2;", self.conn)
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
                if i == 7:
                    daty = QDateEdit(self)
                    daty.setCalendarPopup(True)
                    daty.setDisplayFormat(DATE_FORMAT)
                    daty.setDate(QtCore.QDate(int(_[0:4]), int(_[5:7]), int(_[8:10])))
                    self.view.setCellWidget(rows, i, daty)
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
            if i == 7:
                daty = QDateEdit(self)
                daty.setCalendarPopup(True)
                daty.setDisplayFormat(DATE_FORMAT)
                daty.setDate(QtCore.QDate.currentDate())
                self.view.setCellWidget(self.last_row, i, daty)
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
        self.setup(pos + 50, [1520, height], "Kierowcy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("kierowcy", "pesel", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE kierowcy SET pesel = '" + self.view.item(item.row(), 0).text() + "', imie = '" + self.view.item(item.row(), 1).text() + "', nazwisko = '" + self.view.item(item.row(), 2).text() + "', " \
                                                                                                                                                                                                                     "plec = '" + self.view.cellWidget(item.row(), 3).currentText() + "', uprawnienia_autobusowe = '" + self.view.cellWidget(item.row(), 4).currentText() + "'" \
                                                                                                                                                                                                                                                                                                                                                                            ", uprawnienia_tramwajowe = '" + self.view.cellWidget(item.row(), 5).currentText() + "', placa = " + self.view.item(item.row(), 6).text() + \
                          ", data_zatrudnienia = to_date('" + self.view.cellWidget(item.row(), 7).text() + "', 'YYYY-MM-DD'), stan_cywilny = '" + self.view.cellWidget(item.row(), 8).currentText() + "' WHERE pesel = '" + self.data[item.row()][0] + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO kierowcy VALUES('"+ item(row, 0).text() +"', '"+ item(row, 1).text() +"', '"+ item(row, 2).text() +"', '"+ item(row, 3).currentText() +"' ,'"+ item(row, 4).currentText() + \
                      "', '"+ item(row, 5).currentText() +"', "+ item(row, 6).text() +", to_date('"+ item(row, 7).text() +"', 'YYYY-MM-DD'), '"+ item(row, 8).currentText() +"');"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class KierowcyPojazdy(FunctionWindow):
    def __init__(self, conn):
        super(KierowcyPojazdy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Pojazdu", "ID Linii", "ID Modelu", "ID producenta", "Pesel kierowcy"]
        self.data = select_from_db("SELECT * FROM kierowcy_i_pojazdy ORDER BY 1, 5;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), str(item[3]), item[4], "Modyfikuj", "Usuń"]):
                if i == 0:
                    lista_pojazdy = QComboBox(self)
                    ids = select_from_db("SELECT id_pojazdu FROM pojazdy ORDER BY 1;", conn)
                    lista_pojazdy.addItem(str(item[0]))
                    for id in ids:
                        if id[0] != item[0]:
                            lista_pojazdy.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_pojazdy)
                    continue
                if i == 4:
                    lista_pesele = QComboBox(self)
                    pesele = select_from_db("SELECT pesel FROM kierowcy ORDER BY 1;", conn)
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
        ids = select_from_db("SELECT id_pojazdu FROM pojazdy ORDER BY 1;", conn)
        lista_pojazdy.addItem("")
        for item in ids:
            lista_pojazdy.addItem(str(item[0]))
        self.view.setCellWidget(self.last_row, 0, lista_pojazdy)

        lista_pesele = QComboBox(self)
        pesele = select_from_db("SELECT pesel FROM kierowcy ORDER BY 1;", conn)
        lista_pesele.addItem("")
        for item in pesele:
            lista_pesele.addItem(item[0])
        self.view.setCellWidget(self.last_row, 4, lista_pesele)

        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [670, height], "Kierowcy a pojazdy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                command = "DELETE FROM kierowcy_i_pojazdy WHERE pojazdy_id_pojazdu = " + str(self.data[item.row()][0]) + "  AND kierowcy_pesel = '" + self.data[item.row()][4] + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                id_pojazdu = self.view.cellWidget(item.row(), 0).currentText()
                command = "UPDATE kierowcy_i_pojazdy SET pojazdy_id_pojazdu = " + id_pojazdu + ", pojazdy_linie_id_linii = (SELECT linie_id_linii FROM pojazdy WHERE id_pojazdu = " + id_pojazdu + \
                          "), pojazdy_id_modelu = (SELECT modele_poj_id_modelu FROM pojazdy WHERE id_pojazdu = " + id_pojazdu + "), " \
                                                                                                                                "pojazdy_id_producenta = (SELECT modele_poj_prod_id_producenta FROM pojazdy WHERE id_pojazdu = " + id_pojazdu + "), " \
                                                                                                                                                                                                                                                "kierowcy_pesel = '" + self.view.cellWidget(item.row(), 4).currentText() + "' WHERE pojazdy_id_pojazdu = " + str(self.data[item.row()][0]) + \
                          " AND kierowcy_pesel = '" + self.data[item.row()][4] + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            command = "INSERT INTO kierowcy_i_pojazdy VALUES(" + item(self.last_row, 0).currentText() + ", (SELECT linie_id_linii FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), " \
                                                                                                                                                                                                             "(SELECT modele_poj_id_modelu FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), " \
                                                                                                                                                                                                                                                                                                                      "(SELECT modele_poj_prod_id_producenta FROM pojazdy WHERE id_pojazdu = " + item(self.last_row, 0).currentText() + "), "+ item(self.last_row, 4).currentText() + ");"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Kolejnosc(FunctionWindow):
    def __init__(self, conn):
        super(Kolejnosc, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Kolejnosc", "ID Linii", "Przystanek", "Miasto", "Strefa"]
        self.data = select_from_db("SELECT * FROM przystanki_w_linii ORDER BY 2, 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), item[3], item[4], "Modyfikuj", "Usuń"]):
                if i == 1:
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT id_linii FROM linie ORDER BY 1;", conn)
                    lista.addItem(_)
                    for id in ids:
                        if id[0] != item[i]:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 2:
                    nazwa = select_from_db("SELECT nazwa_przystanku FROM przystanki WHERE id_przystanku = '" + _ + "';", conn)
                    nazwa = str(nazwa[0])[2:-3]
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT nazwa_przystanku FROM przystanki ORDER BY 1;", conn)
                    lista.addItem(nazwa)
                    for id in ids:
                        if id[0] != nazwa:
                            lista.addItem(id[0])
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)

        for i in range(0, len(self.labels)-2):
            if i == 1:
                lista = QComboBox(self)
                ids = select_from_db("SELECT id_linii FROM linie ORDER BY 1;", conn)
                lista.addItem("")
                for id in ids:
                    lista.addItem(str(id[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 2:
                lista = QComboBox(self)
                ids = select_from_db("SELECT nazwa_przystanku FROM przystanki ORDER BY 1;", conn)
                lista.addItem("")
                for id in ids:
                    lista.addItem(id[0])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [670, height], "kolejność przystanków")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                command = "DELETE FROM przystanki_w_linii WHERE kolejnosc = " + str(self.data[item.row()][0]) + "AND linie_id_linii = " + str(self.data[item.row()][1]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                id_przys = self.view.cellWidget(item.row(), 2).currentText()
                command = "UPDATE przystanki_w_linii SET kolejnosc = " + self.view.item(item.row(), 0).text() + ", linie_id_linii = " + self.view.cellWidget(item.row(), 1).currentText() + ", " \
                          "przystanki_id_przystanku = (SELECT id_przystanku FROM przystanki WHERE nazwa_przystanku = '"+ id_przys + "'), przystanki_miasta_nazwa_miasta = (SELECT miasta_nazwa_miasta FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "'), " \
                          "przystanki_strefy_typ_strefy = (SELECT strefy_typ_strefy FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "') WHERE kolejnosc = " + str(self.data[item.row()][0]) + "AND linie_id_linii = " + str(self.data[item.row()][1]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            id_przys = item(self.last_row, 2).currentText()
            command = "INSERT INTO przystanki_w_linii VALUES("+ item(self.last_row, 0).text() + ", " + item(self.last_row, 1).currentText() + ", (SELECT id_przystanku FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "'), " + \
                      "(SELECT miasta_nazwa_miasta FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "'), (SELECT strefy_typ_strefy FROM przystanki WHERE nazwa_przystanku = '" + id_przys + "'));"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Linie(FunctionWindow):
    def __init__(self, conn):
        super(Linie, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID linii", "Typ linii"]
        self.data = select_from_db("SELECT * FROM linie ORDER BY 1;", self.conn)
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

        self.setup(pos + 50, [500, height], "Linie")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("linie", "id_linii", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE linie SET id_linii = " + self.view.item(item.row(), 0).text() + ", typ_linii = '" + self.view.cellWidget(item.row(), 1).currentText() + "' WHERE id_linii = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
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
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Miasta(FunctionWindow):
    def __init__(self, conn):
        super(Miasta, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Nazwa", "Status", "Liczba mieszkańców", "Powierzchnia", "Gęstość zaludnienia"]
        self.data = select_from_db("SELECT * FROM miasta ORDER BY 1;", self.conn)
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

        self.setup(pos + 50, [900, height], "Miasta")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("miasta", "nazwa_miasta", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE miasta SET nazwa_miasta = '" + self.view.item(item.row(), 0).text() + "', status = '" + self.view.cellWidget(item.row(), 1).currentText() + "', liczba_mieszkancow = " + self.view.item(item.row(), 2).text() + ", " \
                                                                                                                                                                                                                                                  "powierzchnia = " + self.view.item(item.row(), 3).text() + ", gestosc_zaludnienia = " + self.view.item(item.row(), 4).text() + " WHERE nazwa_miasta = '" + self.data[item.row()][0] + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO miasta (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) " \
                      "VALUES('" + item(row, 0).text() + "', '" + item(row, 1).currentText() + "', " + item(row, 2).text() + ", " + item(row, 3).text() + ");"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Modele(FunctionWindow):
    def __init__(self, conn):
        super(Modele, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID Modelu", "Nazwa Modelu", "Typ pojazdu", "Czy niskopodłogowy", "Miejsca siedzące", "Miejsca stojące", "Producent"]
        self.data = select_from_db("SELECT * FROM modele_pojazdow ORDER BY 1;", self.conn)
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
                    nazwa = select_from_db("SELECT nazwa_producenta FROM producenci WHERE id_producenta = " + _ + ";", conn)
                    nazwa = str(nazwa[0])[2:-3]
                    lista = QComboBox(self)
                    lista.addItem(nazwa)
                    ids = select_from_db("SELECT nazwa_producenta FROM producenci ORDER BY 1;", conn)
                    for id in ids:
                        if id[0] != nazwa:
                            lista.addItem(id[0])
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
                ids = select_from_db("SELECT nazwa_producenta FROM producenci ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(item[0])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, [1200, height], "Modele")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("modele_pojazdow", "id_modelu", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE modele_pojazdow SET id_modelu = " + self.view.item(item.row(), 0).text() + ", nazwa_modelu = '" + self.view.item(item.row(), 1).text() + "', typ_pojazdu = '" + self.view.cellWidget(item.row(), 2).currentText() + "', " \
                "czy_niskopodlogowy = '" + self.view.cellWidget(item.row(), 3).currentText() + "', liczba_miejsc_siedzacych = " + self.view.item(item.row(), 4).text() + ", " \
                "liczba_miejsc_stojacych = " + self.view.item(item.row(), 5).text() + ", producenci_id_producenta = (SELECT id_producenta FROM producenci WHERE nazwa_producenta = '" + self.view.cellWidget(item.row(), 6).currentText() + "') WHERE id_modelu = '" + str(self.data[item.row()][0]) + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO modele_pojazdow VALUES(NEXTVAL('model_seq'), '" + item(row, 1).text() + "', '" + item(row, 2).currentText() + "', '" + \
            item(row, 3).currentText() + "', " + item(row, 4).text() + ", " + item(row, 5).text() + ", (SELECT id_producenta FROm producenci WHERE nazwa_producenta = '" + item(row, 6).currentText() + "'));"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Pojazdy(FunctionWindow):
    def __init__(self, conn):
        super(Pojazdy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID pojazdu", "Max liczba osob", "ID Linii", "ID biletomatu", "Rok produkcji", "Data waznosci przegladu", "Model", "ID Producenta"]
        self.data = select_from_db("SELECT * FROM pojazdy ORDER BY 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]), str(item[7]), "Modyfikuj", "Usuń"]):
                if i == 2:
                    lista_linii = QComboBox(self)
                    lista_linii.addItem(str(item[i]))
                    ids = select_from_db("SELECT id_linii FROM linie ORDER BY 1;", conn)
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
                        lista_bil.addItems([_, '-'])
                    ids = select_from_db("SELECT id_biletomatu FROM biletomaty ORDER BY 1;", conn)
                    for id in ids:
                        if str(id[0]) != _:
                            lista_bil.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_bil)
                    continue
                if i == 5:
                    daty = QDateEdit(self)
                    daty.setCalendarPopup(True)
                    daty.setDisplayFormat(DATE_FORMAT)
                    daty.setDate(QtCore.QDate(int(_[0:4]), int(_[5:7]), int(_[8:10])))
                    self.view.setCellWidget(rows, i, daty)
                    continue
                if i == 6:
                    nazwa = select_from_db("SELECT nazwa_modelu FROM modele_pojazdow WHERE id_modelu = " + _ + ";", conn)
                    nazwa = str(nazwa[0])[2:-3]
                    lista = QComboBox(self)
                    lista.addItem(nazwa)
                    ids = select_from_db("SELECT nazwa_modelu FROM modele_pojazdow ORDER BY 1;", conn)
                    for id in ids:
                        if id[0] != nazwa:
                            lista.addItem(id[0])
                    self.view.setCellWidget(rows, i, lista)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(2, len(self.labels)-1):
            if i == 2:
                lista = QComboBox(self)
                ids = select_from_db("SELECT id_linii FROM linie ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 3:
                lista = QComboBox(self)
                ids = select_from_db("SELECT id_biletomatu FROM biletomaty ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 5:
                daty = QDateEdit(self)
                daty.setCalendarPopup(True)
                daty.setDisplayFormat(DATE_FORMAT)
                daty.setDate(QtCore.QDate.currentDate())
                self.view.setCellWidget(self.last_row, i, daty)
                continue
            if i == 6:
                lista = QComboBox(self)
                ids = select_from_db("SELECT nazwa_modelu FROM modele_pojazdow ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(item[0])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()

        self.setup(pos + 50, [1150, height], "Pojazdy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("pojazdy", "id_pojazdu", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                bil = self.view.cellWidget(item.row(), 3).currentText()
                n_mod = self.view.cellWidget(item.row(), 6).currentText()
                if bil in ["None", "-"]:
                    bil = "null"
                command = "UPDATE pojazdy SET id_pojazdu = " + self.view.item(item.row(), 0).text() + ", max_liczba_osob = (SELECT sum_sits((SELECT id_modelu FROM modele_pojazdow WHERE nazwa_modelu = '" + n_mod + "'))), " \
                "linie_id_linii = " + self.view.cellWidget(item.row(), 2).currentText() + ", biletomaty_id_biletomatu = " + bil + ", rok_produkcji = " + self.view.item(item.row(), 4).text() + \
                ", data_waznosci_przegladu = to_date('" + self.view.cellWidget(item.row(), 5).text() + "', 'YYYY-MM-DD'), modele_poj_id_modelu = (SELECT id_modelu FROM modele_pojazdow WHERE nazwa_modelu = '" + n_mod + \
                "'), modele_poj_prod_id_producenta = (SELECT producenci_id_producenta FROM modele_pojazdow WHERE nazwa_modelu = '" + n_mod + "') WHERE id_pojazdu = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            bil = item(row, 3).currentText()
            n_mod = item(row, 6).currentText()
            if bil == '':
                bil = "null"
            command = "INSERT INTO pojazdy VALUES(NEXTVAL('pojazd_seq'), (SELECT sum_sits((SELECT id_modelu FROM modele_pojazdow WHERE nazwa_modelu = '" + n_mod + "'))), "+ item(row, 2).currentText() +", "+ bil +", "+ item(row, 4).text() + \
                      ", to_date('"+ item(row, 5).text() +"', 'YYYY-MM-DD'), (SELECT id_modelu FROM modele_pojazdow WHERE nazwa_modelu = '"+ item(row, 6).currentText() +"'), (SELECT producenci_id_producenta FROM modele_pojazdow WHERE nazwa_modelu = '"+ item(row, 6).currentText() +"'));"
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Producenci(FunctionWindow):
    def __init__(self, conn):
        super(Producenci, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID producenta", "Nazwa"]
        self.data = select_from_db("SELECT * FROM producenci ORDER BY 1;", self.conn)
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
        self.setup(pos + 50, [500, height], "Producenci")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("producenci", "id_producenta", str(self.data[item.row()][0]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE producenci SET id_producenta = " + self.view.item(item.row(), 0).text() + ", nazwa_producenta = '" + self.view.item(item.row(), 1).text() + "' WHERE id_producenta = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            command = "INSERT INTO producenci VALUES(NEXTVAL('producer_seq'), '" + item(row, 1).text() + "');"
            cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Przyjazdy(FunctionWindow):
    def __init__(self, conn):
        super(Przyjazdy, self).__init__()
        self.initialze_grid()
        self.conn = conn
        self.labels = ["ID przyjazdu", "ID Linii", "Kolejność w linii", "Godzina przyjazdu", "ID przystanku", "Miasto", "Strefa"]
        self.data = select_from_db("SELECT * FROM przyjazdy ORDER BY 2, 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[4]), str(item[1]), str(item[0]), str(item[5]), str(item[2]), item[3], item[6], "Modyfikuj", "Usuń"]):
                if i == 1:
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT DISTINCT linie_id_linii FROM przystanki_w_linii ORDER BY 1;", conn)
                    lista.addItem(_)
                    for id in ids:
                        if id[0] != item[1]:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 2:
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT kolejnosc FROM przystanki_w_linii WHERE linie_id_linii = "+ str(item[1]) + " ORDER BY 1;", conn)
                    lista.addItem(_)
                    for id in ids:
                        if id[0] != item[i]:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 3:
                    daty = QTimeEdit(self)
                    daty.setCalendarPopup(True)
                    daty.setDisplayFormat(HOUR_FORMAT)
                    daty.setTime(QtCore.QTime(int(_[0:2]), int(_[3:5]), int(_[6:8])))
                    self.view.setCellWidget(rows, i, daty)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, len(self.labels)-3):
            if i == 1:
                lista = QComboBox(self)
                ids = select_from_db("SELECT DISTINCT linie_id_linii FROM przystanki_w_linii ORDER BY 1;", conn)
                lista.addItem("")
                for id in ids:
                    lista.addItem(str(id[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 2:
                self.set_kolejnosc(i)
                continue
            if i == 3:
                daty = QTimeEdit(self)
                daty.setCalendarPopup(True)
                daty.setDisplayFormat(HOUR_FORMAT)
                self.view.setCellWidget(self.last_row, i, daty)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [850, height], "Przyjazdy")
        self.view.selectionModel().selectionChanged.connect(self.update_screen)

    def update_screen(self, selected, deselected):
        for ix in selected.indexes():
            if ix.column() == 2:
                self.set_kolejnosc(2)
                print(self.linia)

    def set_kolejnosc(self, i):
        lista = QComboBox(self)
        self.linia = "null"
        if self.view.cellWidget(self.last_row, 1).currentText() != "":
            self.linia = self.view.cellWidget(self.last_row, 1).currentText()
        ids = select_from_db("SELECT kolejnosc FROM przystanki_w_linii WHERE linie_id_linii = COALESCE("+ str(self.linia) + ", 0) ORDER BY 1;", self.conn)
        lista.addItem("")
        for id in ids:
            lista.addItem(str(id[0]))
        self.view.setCellWidget(self.last_row, i, lista)

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("przyjazdy", "id_przyjazdu", str(self.data[item.row()][4]), self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT przystanki_id_przystanku FROM przystanki_w_linii WHERE kolejnosc = " + self.view.cellWidget(item.row(), 2).currentText() + " AND linie_id_linii = " + self.view.cellWidget(item.row(), 1).currentText() + ";")
                id_przys = cur.fetchone()[0]
                command = "UPDATE przyjazdy SET id_przyjazdu = " + self.view.item(item.row(), 0).text() + ", pwl_linie_id_linii = " + self.view.cellWidget(item.row(), 1).currentText() + ", " \
                          "pwl_kolejnosc = " + self.view.cellWidget(item.row(), 2).currentText() + ", data_przyjazdu = to_timestamp('" + self.view.cellWidget(item.row(), 3).text() + "', 'HH24:MI:SS'), " \
                          "pwl_przystanki_id_przystanku = " + str(id_przys) + ", pwl_przystanki_nazwa_miasta = (SELECT miasta_nazwa_miasta FROM przystanki WHERE id_przystanku = " + str(id_przys) + "), " \
                          "pwl_przyst_strefy_typ_strefy = (SELECT strefy_typ_strefy FROM przystanki WHERE id_przystanku = " + str(id_przys) + ") WHERE id_przyjazdu = " + str(self.data[item.row()][4]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            cur.execute("SELECT przystanki_id_przystanku FROM przystanki_w_linii WHERE kolejnosc = " + item(row, 2).currentText() + " AND linie_id_linii = " + item(row, 1).currentText())
            id_przys = cur.fetchone()[0]

            command = "INSERT INTO przyjazdy VALUES(" + item(row, 2).currentText() + ", " + item(row, 1).currentText() + ", " + str(id_przys) + ", (SELECT miasta_nazwa_miasta FROM przystanki WHERE id_przystanku = " + str(id_przys) + "), " + \
                      "NEXTVAL('przyjazd_seq'), to_timestamp('" + item(row, 3).text() + "', 'HH24:MI:SS'), (SELECT strefy_typ_strefy FROM przystanki WHERE id_przystanku = " + str(id_przys) + "));"
            # cur = self.conn.cursor()
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Przystanki(FunctionWindow):
    def __init__(self, conn):
        super(Przystanki, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["ID przystanku", "Nazwa", "Adres", "Miasto", "Czy jest zajezdnią?", "ID biletomatu", "Strefa"]
        self.data = select_from_db("SELECT * FROM przystanki ORDER BY 1;", self.conn)
        self.view.setColumnCount(len(self.labels) + 2)
        self.view.setHorizontalHeaderLabels(self.labels + ["", ""])
        for item in self.data:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            for i, _ in enumerate([str(item[0]), item[1], item[2], item[3], item[4], str(item[5]), item[6], "Modyfikuj", "Usuń"]):
                if i == 3:
                    lista = QComboBox(self)
                    ids = select_from_db("SELECT nazwa_miasta FROM miasta ORDER BY 1;", conn)
                    lista.addItem(_)
                    for id in ids:
                        if id[0] != _:
                            lista.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 4:
                    lista = QComboBox(self)
                    lista.addItem(_)
                    for id in ["tak", "nie"]:
                        if id != _:
                            lista.addItem(id)
                    self.view.setCellWidget(rows, i, lista)
                    continue
                if i == 5:
                    lista_bil = QComboBox(self)
                    if str(_) == "None":
                        lista_bil.addItem('-')
                    else:
                        lista_bil.addItems([_, '-'])
                    ids = select_from_db("SELECT id_biletomatu FROm biletomaty ORDER BY 1;", conn)
                    for id in ids:
                        if str(id[0]) != _:
                            lista_bil.addItem(str(id[0]))
                    self.view.setCellWidget(rows, i, lista_bil)
                    continue
                if i == 6:
                    lista_stref = QComboBox(self)
                    lista_stref.addItem(_)
                    for id in ['A', 'B', 'C']:
                        if id != _:
                            lista_stref.addItem(id)
                    self.view.setCellWidget(rows, i, lista_stref)
                    continue
                self.view.setItem(rows, i, QTableWidgetItem(_))

        self.last_row = self.view.rowCount()
        self.view.setRowCount(self.last_row + 1)
        for i in range(1, len(self.labels)):
            if i == 3:
                lista = QComboBox(self)
                ids = select_from_db("SELECT nazwa_miasta FROM miasta ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(item[0])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 4:
                lista = QComboBox(self)
                lista.addItems(["", "tak", "nie"])
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 5:
                lista = QComboBox(self)
                ids = select_from_db("SELECT id_biletomatu FROM biletomaty ORDER BY 1;", conn)
                lista.addItem("")
                for item in ids:
                    lista.addItem(str(item[0]))
                self.view.setCellWidget(self.last_row, i, lista)
                continue
            if i == 6:
                lista_stref = QComboBox(self)
                lista_stref.addItems(['', 'A', 'B', 'C'])
                self.view.setCellWidget(self.last_row, i, lista_stref)
                continue
            self.view.setCellWidget(self.last_row, i, QLineEdit())
        self.view.setCellWidget(self.last_row, len(self.labels), self.push_button)

        self.view.resizeColumnsToContents()
        self.get_signal()
        self.setup(pos + 50, [1150, height], "Przystanki")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("przystanki", "id_przystanku", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print("Cannot delete this record")
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                bil = self.view.cellWidget(item.row(), 5).currentText()
                if bil in ["None", "-"]:
                    bil = "null"
                command = "UPDATE przystanki SET id_przystanku = " + self.view.item(item.row(), 0).text() + ", nazwa_przystanku = '" + self.view.item(item.row(), 1).text() + "', " \
                "adres = '" + self.view.item(item.row(), 2).text() + "', miasta_nazwa_miasta = '" + self.view.cellWidget(item.row(), 3).currentText() + "', " \
                "czy_zajezdnia = '" + self.view.cellWidget(item.row(), 4).currentText() + "', biletomaty_id_biletomatu = " + bil + ", " \
                "strefy_typ_strefy = '" + self.view.cellWidget(item.row(), 6).currentText() + "' WHERE id_przystanku = " + str(self.data[item.row()][0]) + ";"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
                self.conn.rollback()

    def add_to_db(self):
        try:
            item = self.view.cellWidget
            row = self.last_row
            cur = self.conn.cursor()
            bil = item(row, 5).currentText()
            if bil == "":
                bil = "null"
            command = "INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), '" + item(row, 1).text() + "', '"+ item(row, 2).text() +"', '"+ item(row, 3).currentText() +"', '"+ item(row, 4).currentText() + \
                      "', "+ bil + ", '" + item(row, 6).currentText() + "');"
            print(command)
            cur.execute(command)
            self.conn.commit()
            cur.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()


class Strefy(FunctionWindow):
    def __init__(self, conn):
        super(Strefy, self).__init__()
        self.initialze_grid()

        self.conn = conn
        self.labels = ["Typ strefy"]
        self.data = select_from_db("SELECT * FROM strefy ORDER BY 1;", self.conn)
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
        self.setup(pos + 50, [280, height/2], "Strefy")

    def modify(self, item):
        if item.data() == "Usuń":
            try:
                delete_from_db("strefy", "typ_strefy", self.data[item.row()][0], self.conn)
                self.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s", error)
                print(DELETE_ERROR)
                self.info_label.setText(DELETE_ERROR)
                self.info_label.setVisible(True)
                self.conn.rollback()
        elif item.data() == "Modyfikuj":
            try:
                command = "UPDATE strefy SET typ_strefy = '" + self.view.cellWidget(item.row(), 0).currentText() + "' WHERE typ_strefy = '" + self.data[item.row()][0] + "';"
                cur = self.conn.cursor()
                print(command)
                cur.execute(command)
                self.conn.commit()
                cur.close()
                self.close()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                if 'already exists' in str(error):
                    self.info_label.setText(UPDATE_ERROR_EXISTS)
                elif 'still referenced' in str(error):
                    self.info_label.setText(UPDATE_ERROR_VIOLATES)
                self.info_label.setVisible(True)
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
            self.info_label.setText(INSERT_ERROR)
            self.info_label.setVisible(True)
            self.conn.rollback()
