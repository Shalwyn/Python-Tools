import os
import configparser
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime
from playsound import playsound

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

open(config['FILES']['clienttxt'], "r")
originalTime = os.path.getmtime(config['FILES']['clienttxt'])

lastlinesold = sum(1 for line in open(
    config['FILES']['clienttxt'], 'r', encoding='UTF8'))
lastseenline = ""

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'trade.db')
verbindung = sqlite3.connect(getpath)

while True:
    
    if os.path.getmtime(config['FILES']['clienttxt']) > originalTime:
        
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
        ding = open(config['FILES']['clienttxt'], 'r', encoding='UTF8')
        lastlinesnew = sum(1 for line in ding)

        while lastlinesold < lastlinesnew:
            last_line = open(config['FILES']['clienttxt'],
                            'r', encoding='UTF8').readlines()[lastlinesold]
            
            if config['FILES']['league'] in last_line and "@From" in last_line:
                splitmsg = last_line.split()
                buyer = splitmsg[splitmsg.index("Hi,") - 1]
                del splitmsg[0:splitmsg.index("Hi,")]
                buyer = buyer[:-1]
                item = splitmsg[splitmsg.index("your") + 1:splitmsg.index("listed")]
                price = splitmsg[splitmsg.index("for") + 1:splitmsg.index("for") + 3]
                stash = splitmsg[splitmsg.index(config['FILES']['league']) + 1:splitmsg.index(config['FILES']['league']) + 11]
                
                windowtext = " ".join(item)
                windowprice = " ".join(price)
                windowstash = " ".join(stash)

                now = datetime.now()

                current_time = now.strftime("%d/%m/%Y %H:%M:%S")                    

                cursor = verbindung.cursor()
                cursor.execute(f'insert into trades ("nick", "item", "price", "time") values ("{buyer}", "{windowtext}", "{windowprice}", "{current_time}")')
                verbindung.commit()

                print(f'Buyer: {buyer} - Item {windowtext} - Price: {windowprice} - {current_time}')
                playsound('horn.mp3')
                

            lastlinesold = lastlinesold + 1
            lastseenline = last_line