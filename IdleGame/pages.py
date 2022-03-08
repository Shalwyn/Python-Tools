from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import functions as fu
import tabulate
import sqlite3


user = "Shalora"


def test(self):
    connectSql = self.db

    self.widgetSite.setStyleSheet("background-color: rgb(20, 20, 20)")

    self.label = [0] * 50000
    self.label2 = [0] * 50000
    self.label3 = [0] * 50000
    self.label4 = [0] * 50000
    layout = [0] * 50000
    i = 0
    j = 0

    self.scroll_area = QScrollArea()
    self.framelayout.addWidget(self.scroll_area)
    self.scroll_widget = QWidget()
    self.scroll_layout = QFormLayout(self.scroll_widget)

    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}" ORDER BY lebensalter DESC'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()

    inhalt = ""

    for zeile in zeilen:
        layout[i] = QHBoxLayout()
        layout[i].setSpacing(200)

        j += 1
        self.label[i] = QLabel(f'{j}')
        layout[i].addWidget(self.label[i])

        self.label4[i] = QLabel(f'{zeile[6]}')
        layout[i].addWidget(self.label4[i])

        self.label2[i] = QLabel(f'Alter: {round(zeile[2], 1)}')
        layout[i].addWidget(self.label2[i])

        self.label3[i] = QLabel(f'Zufriedenheit: {round(zeile[5], 1)}')
        layout[i].addWidget(self.label3[i])

        self.label4[i] = QLabel(f'Gesundheit: {round(zeile[4], 1)}')
        layout[i].addWidget(self.label4[i])

        self.scroll_layout.addRow(layout[i])
        i += 1

        self.scroll_layout.setAlignment(Qt.AlignCenter)

    self.scroll_area.setWidget(self.scroll_widget)
    self.scroll_area.setAlignment(Qt.AlignHCenter)


def forschung(self):
    connectSql = self.db
    cursor = connectSql.cursor()
    self.scroll_area = QScrollArea()
    self.framelayout.addWidget(self.scroll_area)
    self.scroll_widget = QWidget()
    self.scroll_layout = QFormLayout(self.scroll_widget)

    self.widgetSite.setStyleSheet("background-color: rgb(20, 20, 20)")
    cursor = connectSql.cursor()
    exucute = 'SELECT * FROM forschung'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    self.label = [0] * 30
    self.label2 = [0] * 30
    self.label3 = [0] * 30
    self.label4 = [0] * 30
    self.buttonFor = [0] * 30
    layout = [0] * 50000

    i = 0
    for zeile in zeilen:
        layout[i] = QHBoxLayout()
        layout[i].setSpacing(200)

        self.label[i] = QLabel(f'{zeile[1]}')
        layout[i].addWidget(self.label[i])

        self.label2[i] = QLabel(f'{zeile[2]} * {zeile[3]}')
        layout[i].addWidget(self.label2[i])

        kostennext = zeile[4] * (zeile[5] + 1)
        self.label3[i] = QLabel(f'{kostennext} Papier')
        layout[i].addWidget(self.label3[i])

        self.buttonFor[i] = QPushButton("Forschen")
        self.buttonFor[i].setStyleSheet("max-width: 60px")
        self.buttonFor[i].clicked.connect(
            lambda checked, text=zeile[0]: forsch(self, text))
        layout[i].addWidget(self.buttonFor[i])

        self.scroll_layout.addRow(layout[i])
        i += 1

    self.scroll_area.setWidget(self.scroll_widget)
    self.scroll_area.setAlignment(Qt.AlignHCenter)


def gebaeude(self):
    connectSql = self.db
    cursor = connectSql.cursor()
    self.scroll_area = QScrollArea()
    self.framelayout.addWidget(self.scroll_area)
    self.scroll_widget = QWidget()
    self.scroll_layout = QFormLayout(self.scroll_widget)

    cursor = connectSql.cursor()
    exucute = 'SELECT * FROM gebaeude where unlock = true '
    cursor.execute(exucute)

    zeilen = cursor.fetchall()
    self.label = [0] * 30
    self.label2 = [0] * 30
    self.label3 = [0] * 30
    self.label4 = [0] * 30
    self.label5 = [0] * 30
    self.buttonBau = [0] * 30
    self.buttonPlus = [0] * 30
    self.buttonMinus = [0] * 30
    layout = [0] * 50000
    i = 0

    for zeile in zeilen:
        layout[i] = QGridLayout()
        layout[i].setSpacing(50)
        maxAr = zeile[3]
        self.label[i] = QLabel(f'{zeile[1]}')
        layout[i].addWidget(self.label[i], 0, 0)

        self.label4[i] = QLabel(f'Holz: {zeile[2]} Stein: {zeile[6]}')
        layout[i].addWidget(self.label4[i], 0, 1)

        exucute = f'SELECT * FROM bauten where userid = {self.userid} and gebid = {zeile[0]}'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        if zeilen:
            anzahl = zeilen[0][3]
            self.label2[i] = QLabel(f'Anzahl: {anzahl}')
            layout[i].addWidget(self.label2[i], 0, 2)
            if zeile[3]:
                arbeiter = zeilen[0][4]
                maxshow = maxAr * anzahl
                self.label3[i] = QLabel(f'Arbeiter: {arbeiter} / {maxshow}')
                layout[i].addWidget(self.label3[i], 0, 3)

                self.buttonPlus[i] = QPushButton("+")
                self.buttonPlus[i].setStyleSheet("max-width: 10px")
                self.buttonPlus[i].clicked.connect(
                    lambda checked, text=zeile[0]: addWorker(self, text))
                layout[i].addWidget(self.buttonPlus[i], 0, 5)

                self.buttonMinus[i] = QPushButton("-")
                self.buttonMinus[i].setStyleSheet("max-width: 10px")
                self.buttonMinus[i].clicked.connect(
                    lambda checked, text=zeile[0]: delWorker(self, text))
                layout[i].addWidget(self.buttonMinus[i], 0, 4)

            else:
                self.label3[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 3)
                self.buttonPlus[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 4)
                self.buttonMinus[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 5)

        else:
            self.label2[i] = QLabel('Anzahl: 0')
            layout[i].addWidget(self.label2[i], 0, 2)

            if zeile[3]:
                self.label3[i] = QLabel('Arbeiter: 0')
                layout[i].addWidget(self.label3[i], 0, 3)

                self.buttonPlus[i] = QPushButton("+")
                self.buttonPlus[i].setStyleSheet("max-width: 10px")
                self.buttonPlus[i].clicked.connect(
                    lambda checked, text=zeile[0]: addWorker(self, text))
                layout[i].addWidget(self.buttonPlus[i], 0, 5)

                self.buttonMinus[i] = QPushButton("-")
                self.buttonMinus[i].setStyleSheet("max-width: 10px")
                self.buttonMinus[i].clicked.connect(
                    lambda checked, text=zeile[0]: delWorker(self, text))
                layout[i].addWidget(self.buttonMinus[i], 0, 4)
            else:
                self.label3[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 3)
                self.buttonPlus[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 4)
                self.buttonMinus[i] = QLabel('')
                layout[i].addWidget(self.label3[i], 0, 5)

        self.buttonBau[i] = QPushButton("Bauen")
        self.buttonBau[i].setStyleSheet("max-width: 40px")

        self.buttonBau[i].clicked.connect(
            lambda checked, text=zeile[0]: gebbau(self, text))
        layout[i].addWidget(self.buttonBau[i], 0, 6)
        self.scroll_layout.addRow(layout[i])
        i += 1

    self.scroll_area.setWidget(self.scroll_widget)
    self.scroll_area.setAlignment(Qt.AlignHCenter)
    self.widgetSite.setStyleSheet("background-color: rgb(20, 20, 20)")


def suchtrupp(self):
    connectSql = self.db
    cursor = connectSql.cursor()
    huettelvl = fu.getBauten(self, 13)
    print(huettelvl)


def statistiken(self):
    connectSql = self.db
    cursor = connectSql.cursor()
    label1 = [0] * 30
    label2 = [0] * 30
    label3 = [0] * 30
    label4 = [0] * 30

    self.widgetSite.setStyleSheet("background-color: rgb(20, 20, 20)")
    gesZufriedenheit = 0
    cursor = connectSql.cursor()

    HolzArb = 0
    zeilen = fu.getBauten(self, 1)
    if zeilen:
        HolzArb = zeilen[0][4]

    bauern = 0
    zeilen = fu.getBauten(self, 2)
    if zeilen:
        bauern = zeilen[0][4]

    fischer = 0
    zeilen = fu.getBauten(self, 5)
    if zeilen:
        fischer = zeilen[0][4]

    wassertraeger = 0
    zeilen = fu.getBauten(self, 4)
    if zeilen:
        wassertraeger = zeilen[0][4]

    steinmetz = 0
    zeilen = fu.getBauten(self, 8)
    if zeilen:
        steinmetz = zeilen[0][4]

    eisenberg = 0
    zeilen = fu.getBauten(self, 10)
    if zeilen:
        eisenberg = zeilen[0][4]

    arbeiterBa = 0
    zeilen = fu.getBauten(self, 12)
    if zeilen:
        arbeiterBa = zeilen[0][4]

    exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    gesamtEinwohner = len(zeilen)

    for zeile in zeilen:
        gesZufriedenheit += zeile[5]

    durZufriedenheit = gesZufriedenheit / gesamtEinwohner
    fakZufriedenheit = durZufriedenheit / 100

    holzpflug = fu.getForschung(self, 1)
    nahrungForAdd = 1 + (holzpflug[3] * holzpflug[5])

    exucute = 'SELECT * FROM bauten WHERE gebid = "9"'
    cursor.execute(exucute)
    bauten = cursor.fetchone()
    arbeiterpa = bauten[4]

    exucute = 'SELECT * FROM bauten WHERE gebid = "11"'
    cursor.execute(exucute)
    bauten = cursor.fetchone()
    arbeiterko = bauten[4]

    nahrungSek = (
            ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (
                        gesamtEinwohner * (1 / 300))) * fakZufriedenheit * nahrungForAdd)
    nahrungMin = (
            ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (
                    gesamtEinwohner * (1 / 300))) * fakZufriedenheit * nahrungForAdd)*60
    nahrungStd = (
            ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (
                    gesamtEinwohner * (1 / 300))) * fakZufriedenheit * nahrungForAdd)*3600
    holzSek = ((HolzArb * ((10 / 10) / 60))
               * fakZufriedenheit - (2 / 5 / 60 * arbeiterpa))
    holzMin = ((HolzArb * ((10 / 10) / 60))
               * fakZufriedenheit - (2 / 5 / 60 * arbeiterpa)) * 60
    holzStd = ((HolzArb * ((10 / 10) / 60))
               * fakZufriedenheit - (2 / 5 / 60 * arbeiterpa) - (2 / 5 / 60 * arbeiterko)) * 3600
    wasserSek = ((wassertraeger * (1 / 200)) * fakZufriedenheit)
    wasserMin = ((wassertraeger * (1 / 200)) * fakZufriedenheit) * 60
    wasserStd = ((wassertraeger * (1 / 200)) * fakZufriedenheit) * 3600
    steinSek = ((steinmetz * (1 / 60)) * fakZufriedenheit)
    steinMin = ((steinmetz * (1 / 60)) * fakZufriedenheit) * 60
    steinStd = ((steinmetz * (1 / 60)) * fakZufriedenheit) * 3600
    eisenSek = ((eisenberg * (1 / 70))
                * fakZufriedenheit - 1 / 5 / 60 * arbeiterBa)
    eisenMin = ((eisenberg * (1 / 70)) * fakZufriedenheit
                - 1 / 5 / 60 * arbeiterBa) * 60
    eisenStd = ((eisenberg * (1 / 70)) * fakZufriedenheit
                - 1 / 5 / 60 * arbeiterBa) * 3600

    papierSek = (1 / 5 / 60 * arbeiterpa)
    papierMin = (1 / 5 / 60 * arbeiterpa) * 60
    papierStd = (1 / 5 / 60 * arbeiterpa) * 3600

    kohleSek = (1 / 5 / 60 * arbeiterko - 1 / 5 / 60 * arbeiterBa)
    kohleMin = (1 / 5 / 60 * arbeiterko - 1 / 5 / 60 * arbeiterBa) * 60
    kohleStd = (1 / 5 / 60 * arbeiterko - 1 / 5 / 60 * arbeiterBa) * 3600

    eisenbarrenSek = (1 / 5 / 60 * arbeiterBa)
    eisenbarrenMin = (1 / 5 / 60 * arbeiterBa) * 60
    eisenbarrenStd = (1 / 5 / 60 * arbeiterBa) * 3600

    label1[0] = QLabel("Rohstoff")
    label1[0].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[0], 0, 0)

    label2[0] = QLabel("Pro Sekunde")
    label2[0].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[0], 0, 1)

    label3[0] = QLabel("Pro Minute")
    label3[0].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[0], 0, 2)

    label4[0] = QLabel("Pro Stunde")
    label4[0].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[0], 0, 3)

    label1[1] = QLabel("Nahrung")
    label1[1].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[1], 1, 0)

    label2[1] = QLabel(f'{round(nahrungSek, 2)}')
    label2[1].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[1], 1, 1)

    label3[1] = QLabel(f'{round(nahrungMin, 2)}')
    label3[1].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[1], 1, 2)

    label4[1] = QLabel(f'{round(nahrungStd, 2)}')
    label4[1].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[1], 1, 3)

    label1[2] = QLabel("Holz")
    label1[2].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[2], 2, 0)

    label2[2] = QLabel(f'{round(holzSek, 2)}')
    label2[2].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[2], 2, 1)

    label3[2] = QLabel(f'{round(holzMin, 2)}')
    label3[2].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[2], 2, 2)

    label4[2] = QLabel(f'{round(holzStd, 2)}')
    label4[2].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[2], 2, 3)

    label1[3] = QLabel("Wasser")
    label1[3].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[3], 3, 0)

    label2[3] = QLabel(f'{round(wasserSek, 2)}')
    label2[3].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[3], 3, 1)

    label3[3] = QLabel(f'{round(wasserMin, 2)}')
    label3[3].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[3], 3, 2)

    label4[3] = QLabel(f'{round(wasserStd, 2)}')
    label4[3].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[3], 3, 3)

    label1[4] = QLabel("Stein")
    label1[4].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[4], 4, 0)

    label2[4] = QLabel(f'{round(steinSek, 2)}')
    label2[4].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[4], 4, 1)

    label3[4] = QLabel(f'{round(steinMin, 2)}')
    label3[4].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[4], 4, 2)

    label4[4] = QLabel(f'{round(steinStd, 2)}')
    label4[4].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[4], 4, 3)

    label1[5] = QLabel("Eisen")
    label1[5].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[5], 5, 0)

    label2[5] = QLabel(f'{round(eisenSek, 2)}')
    label2[5].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[5], 5, 1)

    label3[5] = QLabel(f'{round(eisenMin, 2)}')
    label3[5].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[5], 5, 2)

    label4[5] = QLabel(f'{round(eisenStd, 2)}')
    label4[5].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[5], 5, 3)

    label1[6] = QLabel("Papier")
    label1[6].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[6], 6, 0)

    label2[6] = QLabel(f'{round(papierSek, 2)}')
    label2[6].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[6], 6, 1)

    label3[6] = QLabel(f'{round(papierMin, 2)}')
    label3[6].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[6], 6, 2)

    label4[6] = QLabel(f'{round(papierStd, 2)}')
    label4[6].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[6], 6, 3)

    label1[7] = QLabel("Kohle")
    label1[7].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[7], 7, 0)

    label2[7] = QLabel(f'{round(kohleSek, 2)}')
    label2[7].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[7], 7, 1)

    label3[7] = QLabel(f'{round(kohleMin, 2)}')
    label3[7].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[7], 7, 2)

    label4[7] = QLabel(f'{round(kohleStd, 2)}')
    label4[7].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[7], 7, 3)

    label1[8] = QLabel("Eisenbarren")
    label1[8].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label1[8], 8, 0)

    label2[8] = QLabel(f'{round(eisenbarrenSek, 2)}')
    label2[8].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label2[8], 8, 1)

    label3[8] = QLabel(f'{round(eisenbarrenMin, 2)}')
    label3[8].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label3[8], 8, 2)

    label4[8] = QLabel(f'{round(eisenbarrenStd, 2)}')
    label4[8].setAlignment(Qt.AlignTop)
    self.framelayout.addWidget(label4[8], 8, 3)


def addWorker(self, gebId):
    connectSql = self.db
    cursor = connectSql.cursor()
    huette = 0
    vorhandenArbeiter = 0
    maxArbeiter = 0

    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM bauten where userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()

    for zeile in zeilen:
        vorhandenArbeiter += zeile[4]

    exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    for zeile in zeilen:
        if zeile[2] > 12:
            maxArbeiter += 1

    if (vorhandenArbeiter + 1) <= maxArbeiter:
        exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        if zeilen:
            gebAnz = zeilen[0][3]
            arbeiter = zeilen[0][4]

            exucute = f'SELECT * FROM gebaeude where id = "{gebId}"'
            cursor.execute(exucute)
            gebZeilen = cursor.fetchall()

            maxNew = gebAnz * gebZeilen[0][3]

            if (arbeiter + 1) <= maxNew:
                arbeiter += 1
                exucute = f'UPDATE bauten set arbeiter = "{arbeiter}" where gebid = "{gebId}" and userid = "{self.userid}"'
                cursor.execute(exucute)
                connectSql.commit()

                exucute = f'SELECT * FROM einwohner where job = "0" and userid = "{self.userid}" and lebensalter > "12"'
                cursor.execute(exucute)
                lastZeilen = cursor.fetchall()
                lastid = lastZeilen[len(lastZeilen)-1][0]

                exucute = f'UPDATE einwohner set job = "{zeilen[0][0]}" where userid = "{self.userid}" AND einwohnerid = "{lastid}"'
                cursor.execute(exucute)
                connectSql.commit()

                self.scroll_area.deleteLater()
                self.scroll_area = None
                gebaeude(self)
            else:
                fu.saveNotify(self, "Kein Platz mehr vorhanden")

        else:
            fu.saveNotify(self, "Gebäude nicht gebaut")

    else:
        fu.saveNotify(self, "Keine Arbeiter vorhanden")


def delWorker(self, gebId):
    connectSql = self.db
    cursor = connectSql.cursor()
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    if zeilen:
        arbeiter = zeilen[0][4]
        if (arbeiter - 1) >= 0:
            arbeiter -= 1
            exucute = f'UPDATE bauten set arbeiter = "{arbeiter}" where gebid = "{gebId}" and userid = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()

            exucute = f'SELECT * FROM einwohner where job = "{zeilen[0][0]}" and userid = "{self.userid}"'
            cursor.execute(exucute)
            lastZeilen = cursor.fetchall()
            lastid = lastZeilen[len(lastZeilen)-1][0]

            exucute = f'UPDATE einwohner set job = "0" WHERE userid = "{self.userid}" AND einwohnerid = "{lastid}"'
            cursor.execute(exucute)
            connectSql.commit()
            self.scroll_area.deleteLater()
            self.scroll_area = None
            gebaeude(self)


def gebbau(self, gebId):
    connectSql = self.db
    cursor = connectSql.cursor()
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM gebaeude where id = "{gebId}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    holzKost = zeilen[0][2]
    steinKost = zeilen[0][6]

    rohstoffe = fu.getRohstoffe(self)

    if holzKost <= rohstoffe["holz"] and steinKost <= rohstoffe["stein"]:

        exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        if zeilen:
            anzahl = zeilen[0][3] + 1
            exucute = f'update bauten set anzahl = "{anzahl}" where gebid = "{gebId}" and userid = "{self.userid}"'
            cursor.execute(exucute)

            rohstoffe["holz"] = rohstoffe["holz"] - holzKost
            rohstoffe["stein"] = rohstoffe["stein"] - steinKost
            exucute = f'update user set holz = "{rohstoffe["holz"]}", stein = {rohstoffe["stein"]} where id = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()
        else:
            exucute = f'insert into bauten ("userid", "gebid", anzahl, arbeiter) VALUES ("{self.userid}", "{gebId}", 1, 0)'
            cursor.execute(exucute)

            rohstoffe["holz"] = rohstoffe["holz"] - holzKost
            rohstoffe["stein"] = rohstoffe["stein"] - steinKost
            exucute = f'update user set holz = "{rohstoffe["holz"]}", stein = {rohstoffe["stein"]} where id = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()

        if gebId == 6 or gebId == 7:
            if gebId == 6:
                fu.changeStimmungAll(self, 3)
            if gebId == 7:
                fu.changeStimmungAll(self, 5)

        exucute = f'SELECT * FROM Grundbeduerfnis WHERE running = "1" and gebaude = {gebId}'

        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        if zeilen:

            newLevel = zeilen[0][4] + 1

            exucute = f'update Grundbeduerfnis SET erfuellt = {newLevel} where id = {zeilen[0][0]}'
            cursor.execute(exucute)
            connectSql.commit()

    else:
        fu.saveNotify(self, "Nicht genügend Rohstoffe vorhanden")
    self.scroll_area.deleteLater()
    self.scroll_area = None
    gebaeude(self)


def forsch(self, forid):
    connectSql = self.db
    cursor = connectSql.cursor()
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM forschung WHERE forid = "{forid}"'

    cursor.execute(exucute)
    zeile = cursor.fetchone()
    rohstoffe = fu.getRohstoffe(self)
    kostenpa = (zeile[5] + 1) * zeile[4]
    level = zeile[5]

    if (rohstoffe["papier"] >= kostenpa):
        level = level + 1

        exucute = f'UPDATE forschung SET level = {level} where forid = {forid}'

        cursor.execute(exucute)
        connectSql.commit()

        rohstoffe["papier"] -= kostenpa
        exucute = f'UPDATE user SET papier = {rohstoffe["papier"]} where id = {self.userid}'
        cursor.execute(exucute)
        connectSql.commit()
        self.scroll_area.deleteLater()
        self.scroll_area = None
        forschung(self)
    else:
        fu.saveNotify(self, "Nicht genügend Papier vorhanden")
