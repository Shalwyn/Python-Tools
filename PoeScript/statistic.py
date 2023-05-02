import os
import configparser
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime
from playsound import playsound
import threading
from colorama import Fore, Back, Style
import pygame
import functions as func
if sys.platform == "linux":
    from pynput.keyboard import Key, KeyCode, Listener, Controller
    import subprocess
    import time

keyboard = Controller()
    
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

whispernicks = []
lastwhispernick = ""
x = threading.Thread(target=func.thread_function, name="input_thread", args=(whispernicks, lastwhispernick, ))
x.start()



#y = threading.Thread(target=func.onlineCount, name="online_counter_threade")
#y.start()

            
while True:
    


    if os.path.getmtime(config['FILES']['clienttxt']) > originalTime:

        
        
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
        ding = open(config['FILES']['clienttxt'], 'r', encoding='UTF8')
        lastlinesnew = sum(1 for line in ding)

        while lastlinesold < lastlinesnew:
            last_line = open(config['FILES']['clienttxt'],
                            'r', encoding='UTF8').readlines()[lastlinesold]

            if "has been slain" in last_line:
                cursor = verbindung.cursor()
                exucute = f'SELECT * FROM deaths'
                cursor.execute(exucute)
                zeile = cursor.fetchone()

                deaths = zeile[0]

                deaths += 1

                cursor = verbindung.cursor()
                cursor.execute(f'update deaths set counter = "{deaths}"')
                
                verbindung.commit()   

                print(Fore.RED + f'Aktuelle Tode: {deaths}')
                print(Style.RESET_ALL)

                getpath = os.path.join(bundle_dir, 'fail-trombone-01.mp3')
                pygame.mixer.init()
                pygame.mixer.music.load(getpath)
                pygame.mixer.music.play()
            
            if config['FILES']['league'] in last_line and "@From" in last_line and "buy" in last_line and "position" in last_line:
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
                x = len(whispernicks) 
                
                whispernicks.append(buyer)
                
                lastwhispernick = buyer
                verbindung.commit()
                
                

                print(Fore.MAGENTA + f'{x}. Buyer: {buyer} - Item {windowtext} - Price: {windowprice} - {current_time}')
                print(Style.RESET_ALL)
                getpath = os.path.join(bundle_dir, 'horn.mp3')
                pygame.mixer.init()
                pygame.mixer.music.load(getpath)
                pygame.mixer.music.play()
                

                cursor = verbindung.cursor()
                exucute = f'SELECT * FROM incoming'
                cursor.execute(exucute)
                zeile = cursor.fetchone()

                chaos = float(zeile[0])
                exalted = float(zeile[1])
                divine = float(zeile[2])

                if "chaos" in windowprice:
                    add = float(windowprice[:windowprice.find("chaos")-1])
                    chaos = chaos + add
                if "exalted" in windowprice: 
                    exalted = exalted + float(windowprice[:windowprice.find("exalted")])
                if "divine" in windowprice: 
                    divine = divine + float(windowprice[:windowprice.find("divine")])

                

                cursor = verbindung.cursor()
                cursor.execute(f'update incoming set chaos = "{chaos}", exalted = {exalted}, divine = {divine}')
                
                verbindung.commit()    

                
                

            lastlinesold = lastlinesold + 1
            lastseenline = last_line