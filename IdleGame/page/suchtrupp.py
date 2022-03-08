import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import functions as fu
import time

user = "Shalora"


def suchtrupp(self):
    connectSql = self.db
    cursor = connectSql.cursor()
    huettelvl = fu.getBauten(self, 13)
    if huettelvl:
        exucute = f'SELECT * FROM suchtruppmission where start > 0'
        cursor.execute(exucute)
        zeilen = cursor.fetchone()
        if not zeilen:

            self.label1 = QLabel("Rohstoff")
            self.label1.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label1, 0, 0)

            self.checkbox = QComboBox(self)
            self.checkbox.addItem("nahrung")
            self.checkbox.addItem("holz")
            self.checkbox.addItem("stein")
            self.framelayout.addWidget(self.checkbox, 0, 1)

            self.checkbox.adjustSize()

            self.label2 = QLabel("Anzahl Arbeiter")
            self.label2.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label2, 0, 2)

            self.textbox = QLineEdit(self)
            self.textbox.setFixedWidth(50)
            self.framelayout.addWidget(self.textbox, 0, 3)

            self.label3 = QLabel("Minuten")
            self.label3.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label3, 0, 4)

            self.checkbox2 = QComboBox(self)
            self.checkbox2.addItem("10")
            self.checkbox2.addItem("20")
            self.checkbox2.addItem("30")
            self.checkbox2.setStyleSheet("max-width: 50px")
            self.framelayout.addWidget(self.checkbox2, 0, 5)

            self.buttonsuch = QPushButton("Suchen")
            self.buttonsuch.setStyleSheet("max-width: 50px")
            self.framelayout.addWidget(self.buttonsuch, 0, 6)

            self.buttonsuch.clicked.connect(
                lambda checked, text="text": suchstart(self))
        else:
            ts = time.time()
            start = zeilen[4]

            rest = (start + (zeilen[3] * 60)) - ts
            min = round(rest / 60)

            self.label1 = QLabel(
                f"Suchtrupp Unterwegs: ")
            self.label1.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label1, 0, 0)

            self.label2 = QLabel(
                f"Arbeiter: {zeilen[1]} ")
            self.label2.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label2, 0, 1)

            self.label3 = QLabel(
                f"Rohstoff: {zeilen[2]} ")
            self.label3.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.label3, 0, 2)

            self.timeLeftLabel = QLabel(
                f"{min} Minuten rest")
            self.timeLeftLabel.setAlignment(Qt.AlignTop)
            self.framelayout.addWidget(self.timeLeftLabel, 0, 3)

            self.timerSuchTruppe = QTimer()
            self.timerSuchTruppe.setInterval(10000)
            self.timerSuchTruppe.timeout.connect(self.calculateSuch)
            self.timerSuchTruppe.start()

    def timerSuchTruppe(self):
        exucute = f'SELECT * FROM suchtruppmission where start > 0'
        cursor.execute(exucute)
        zeilen = cursor.fetchone()

        ts = time.time()
        start = zeilen[4]

        rest = (start + (zeilen[3] * 60)) - ts
        min = round(rest / 60)

        self.timeLeftLabel.setText(f"{min} Minuten rest")


def suchstart(self):
    connectSql = self.db
    cursor = connectSql.cursor()

    ts = time.time()
    suchar = 0
    zeilen = fu.getBauten(self, 13)
    if zeilen:
        suchar = zeilen[0][4]

    if int(self.textbox.text()) <= suchar:
        exucute = f'INSERT INTO suchtruppmission ("arbeiter", "rohstoff", "dauer", "start") VALUES ("{self.textbox.text()}", "{self.checkbox.currentText()}", "{self.checkbox2.currentText()}", "{ts}")'
        cursor.execute(exucute)
        connectSql.commit()
        self.clearLayout(self.framelayout)
        suchtrupp(self)
    else:
        fu.saveNotify(self, "Nicht genügend Arbeiter zugewiesen")
