import matplotlib.pyplot as plt
import sqlite3
import os


def showDiagram(Produkt):
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    getpath = os.path.join(bundle_dir, 'preise.db')
    disk_db = sqlite3.connect(getpath)

    daten = []
    xwerte = []
    altWert = 0
    datumalt = ""

    cursor = disk_db.cursor()
    exucute = f'SELECT * FROM preisverlauf WHERE produkt = "{Produkt}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    for zeile in zeilen:

        datum = zeile[1]
        datum = datum[0:10]

        if zeile[3] != altWert or datum != datumalt:
            daten.append(zeile[3])
            xwerte.append(zeile[1])
            altWert = zeile[3]
            datumalt = datum

    #plt.plot(xwerte, daten)

    fig, ax = plt.subplots()
    ax.plot(xwerte, daten)

    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_rotation(90)

    plt.xlabel("Datum")
    plt.tight_layout()
    plt.show()
