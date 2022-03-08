#!/usr/bin/env python
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import diagramm as dia
import subprocess
import os
import uber
import requests
import cv2
import pyautogui
import numpy as np
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import imaplib
import ama
import psutil
#import test
from email import policy
from vlc import EventType, Media, MediaPlayer, MediaParseFlag, Meta
import subprocess
import time
from threading import Thread
from datetime import datetime
import ama
import requests
import re
from bs4 import BeautifulSoup


class Dialog(QtWidgets.QMainWindow):
    client_id = "wjnywuf0fo0ezlam62n5fqlr5rwfq5"
    client_secret = "nvdfnk1vbhzj16md1j50ytwgwrx0py"
    streamer_name = 'shalora_'

    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials',
        "scope": 'analytics:read:extensions analytics:read:games bits:read channel:edit:commercial channel:manage:broadcast channel:manage:extensions channel:manage:polls channel:manage:predictions channel:manage:redemptions channel:manage:schedule channel:manage:videos channel:read:editors channel:read:goals channel:read:hype_train channel:read:polls channel:read:predictions channel:read:redemptions channel:read:stream_key channel:read:subscriptions clips:edit moderation:read moderator:manage:automod user:edit user:edit:follows user:manage:blocked_users user:read:blocked_users user:read:broadcast user:read:email user:read:follows user:read:subscriptions'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    keys = r.json()

    access_token2 = "79k6ibmi3ad2cjx8b3z1ah2dw09zph"
    access_token = keys['access_token']
    refresh = "m87z85svzr756plqol4z7j9c8c8xqbt6hst551my4rijmf7s4c"

    def get_streams(self, streamid):
        params = {
            "user_id": streamid
        }

        headers = {
            "Authorization": "Bearer {}".format(self.access_token),
            "Client-Id": self.client_id
        }

        response = requests.get(
            "https://api.twitch.tv/helix/streams", params=params, headers=headers)

        return response.json()["data"]

    """Dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'mainNew.ui')

        self = uic.loadUi(getpath, self)
        self.setWindowTitle('Widget Bar')

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('bar.png'))

        self.uberButton.clicked.connect(self.on_pushButton_clicked)
        #self.screenshotButton.clicked.connect(self.make_screenshot)
        #self.screenrecButton.clicked.connect(self.make_video)
        #self.startbotButton.clicked.connect(self.start_bot)

        self.RadioBox.addItem("Electrozombies")
        self.RadioBox.addItem("Dunklewelle")
        self.RadioBox.addItem("Schattenreich")

        self.gameCombo.addItem("Path of Exile")
        self.gameCombo.addItem("Last Epoch")
        self.gameCombo.addItem("Lost Ark")
        self.gameCombo.addItem("Anno 1800")
        self.gameCombo.addItem("Foundation")
        self.gameCombo.addItem("Kingdoms Reborn")
        self.gameCombo.addItem("The Universim")

        self.diaCombo.addItem(
            "Monster Energy Ultra Paradise, 12x500 ml, Einweg-Dose, Zero Zucker und Zero Kalorien")
        self.diaCombo.addItem(
            "Monster Energy Ultra Red, 12x500 ml, Einweg-Dose, Zero Zucker und Zero Kalorien")
        self.diaCombo.addItem(
            "Monster Energy Ultra White, 12x553 ml, Einweg-Dose, Zero Zucker und Zero Kalorien – wiederverschließbar")
        self.diaCombo.addItem(
            "Monster Energy Pipeline Punch, 12x500 ml, Einweg-Dose, mit einem Mix aus Maracuja, Orange und Guave")
        self.diaCombo.addItem(
            "Monster Energy Ultra Fiesta, 12x500 ml, Einweg-Dose, Zero Zucker und Zero Kalorien")
        self.diaCombo.addItem(
            "Monster Energy Rehab Peach, 12x500 ml, Einweg-Dose – Energy Iced Tea mit Pfirsichgeschmack")
        self.diaCombo.addItem(
            "LEGO 76389 Harry Potter Schloss Hogwarts Kammer des Schreckens Spielzeug, Set mit Voldemort als goldene Minifigur und der Großen Halle")

        self.diagrammButton.clicked.connect(self.drawDia)

        self.diaCombo.setStyleSheet("QComboBox"
                                    "{"
                                    "background-color: rgb(49, 49, 49);"
                                    "color: rgb(255, 85, 255);"
                                    "}")

        self.gameCombo.setStyleSheet("QComboBox"
                                     "{"
                                     "background-color: rgb(49, 49, 49);"
                                     "color: rgb(255, 85, 255);"
                                     "}")
        self.uberButton_2.clicked.connect(self.start_Game)
        self.startradioButton.clicked.connect(lambda: self.threadvlc())
        self.stopradioButton.clicked.connect(lambda: self.stopVlc())
        #self.startbrowserButton.clicked.connect(self.start_browser)

        self.twitchLabel.mousePressEvent = self.open_stream1
        self.twitchLabel_2.mousePressEvent = self.open_stream2

        self.progressBar.setMinimum(1)
        self.progressBar.setMaximum(100)
        #self.progressBar.setValue(round(psutil.virtual_memory().percent))

        self.spotifyLabel.mousePressEvent = self.open_spotify

        self.likeButton.clicked.connect(self.like_song)
        self.saveButton.clicked.connect(self.searchSong)

        self.forwardButton.clicked.connect(self.skip_song)

        self.forwardButton_2.clicked.connect(self.prev_song)

        self.read_request()
        self.get_song()

        self.check_mail()

        self.timer = QTimer()
        self.timer.setInterval(300000)
        self.timer.timeout.connect(self.read_request)
        self.timer.start()

        self.check_streamer()
        self.timer2 = QTimer()
        self.timer2.setInterval(60000)
        self.timer2.timeout.connect(self.check_streamer)
        self.timer2.start()

        self.check_sprit()
        self.timer4 = QTimer()
        self.timer4.setInterval(600000)
        self.timer4.timeout.connect(self.check_sprit)
        self.timer4.start()

        self.timer3 = QTimer()
        self.timer3.setInterval(10000)
        self.timer3.timeout.connect(self.get_song)
        self.timer3.start()

        self.timer_ram = QTimer()
        self.timer_ram.setInterval(1000)
        self.timer_ram.timeout.connect(self.get_ram)
        self.timer_ram.start()

        self.timer_time = QTimer()
        self.timer_time.setInterval(1000)
        self.timer_time.timeout.connect(self.set_time)
        self.timer_time.start()

        self.timerama = QTimer()
        self.timerama.setInterval(3600000)
        self.timerama.timeout.connect(self.start_read_ama)
        self.timerama.start()

        self.ui = uber.Ui()
        self.searchWindo = self.searchSong

    def drawDia(self):
        dia.showDiagram(self.diaCombo.currentText())

    def start_read_ama(self):
        ama.amazonread(self)

    def set_time(self):

        now = datetime.now()
        current_time = now.strftime("%d/%m/%y %H:%M:%S")

        self.datumLabel.setText(current_time)

    def searchSong(self):
        actualSong = self.v
        actualSong = actualSong.replace("-", "")

        self.labelsearch = [0] * 10
        self.buttonsearch = [0] * 10
        i = 0

        self.searchWindow = QWidget()

        self.searchWindow.setWindowTitle('Song Search')
        self.searchWindow.setGeometry(100, 100, 600, 100)
        self.searchWindow.setStyleSheet("background-color: black")
        self.gLayout = QGridLayout()

        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "playlist-read-private user-read-recently-played user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        results = sp.search(actualSong, 5, 0, type='track')

        for zeile in results['tracks']['items']:
            trackName = zeile['name']
            trackUri = zeile['uri']
            trackAlbum = zeile['album']['name']
            trackArtist = zeile['artists'][0]['name']
            self.labelsearch[i] = QLabel(
                f'{trackArtist} - {trackName} ({trackAlbum})')
            self.labelsearch[i].setStyleSheet("color: rgb(255,20,147);")
            self.gLayout.addWidget(self.labelsearch[i], i, 0)
            self.buttonsearch[i] = QPushButton('⛘')
            self.buttonsearch[i].clicked.connect(
                lambda checked, text=trackUri: self.saveSong(text))
            self.buttonsearch[i].setStyleSheet("QPushButton { color: rgb(255,20,147); background-color: rgb(31,31,31); border-style: "
                                               "outset; border-width: 1px; min-width: 100px;}"
                                               "QPushButton:pressed { "
                                               "background-color: rgb(255,20,147); color: rgb(31,31,31);"
                                               "}")
            self.gLayout.addWidget(self.buttonsearch[i], i, 1)

            i = i + 1

        self.searchWindow.setLayout(self.gLayout)
        self.searchWindow.show()

    def saveSong(self, trackUri):
        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'
        scope = "playlist-read-private user-read-recently-played user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=client_ID, client_secret=client_SECRET,
                    redirect_uri=redirect_url, scope=scope))

        uri = []
        uri.append(trackUri)
        sp.playlist_add_items('2Yp2HRK0ahORVFOHY8NjgJ', uri)
        print("Song Save in Playlist")

    def getActualVlc(self):
        search = self.v

        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "playlist-read-private user-read-recently-played user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        results = sp.search(search, 1, 0, type='track')

        id = []

        if results['tracks']['items']:
            id.append(results['tracks']['items'][0]['uri'])
            sp.playlist_add_items('2Yp2HRK0ahORVFOHY8NjgJ', id)
            print(f'Song: {v} added to Playlist')
        else:
            print("No Song found")

    def threadvlc(self):
        self.x = Thread(target=self.playVlc)
        self.x.start()

    def playVlc(self):
        self.stop_thread = False

        def _media_cb(event, *unused):
            # XXX callback ... never called
            print(event)

        self.media_player = MediaPlayer()
        if self.RadioBox.currentText() == "Electrozombies":
            media = Media(
                "http://electrozombies.stream.laut.fm/electrozombies?pl=pls&t302=2021-09-16_10-57-42&uuid=3008b1dc-3852-4fab-9d7e-eaa375c80504")
        if self.RadioBox.currentText() == "Dunklewelle":
            media = Media(
                "http://dunklewelle.stream.laut.fm/dunklewelle?pl=pls&t302=2021-09-23_12-23-18&uuid=91e21a39-041b-4ce8-89d1-edb619d23830")
        if self.RadioBox.currentText() == "Schattenreich":
            media = Media(
                "http://schattenreich.stream.laut.fm/schattenreich?pl=m3u&t302=2021-10-02_13-23-16&uuid=c308d4c0-2001-4aa8-98f0-a99529cce070"
            )
        self.media_player.set_media(media)
        self.media_player.play()

        e = self.media_player.event_manager()
        e.event_attach(EventType.MediaMetaChanged, _media_cb, media)
        e.event_attach(EventType.MediaParsedChanged, _media_cb, media)

        meta = {Meta.Album: None,
                Meta.Genre: None,
                Meta.NowPlaying: None}

        while True:
            if self.stop_thread:
                break
            media.parse_with_options(MediaParseFlag.network, 2)
            for k in meta.keys():
                self.v = media.get_meta(k)
            if self.v != meta[k]:
                print("{}".format(self.v))

                notify = "Now Playing: " + self.v
                self.radioLabel.setText(f'Current Radio Song: {self.v}')
                subprocess.Popen(['notify-send', notify])
                meta[k] = self.v
            time.sleep(2)

    def stopVlc(self):
        self.media_player.stop()
        self.stop_thread = True

    def open_spotify(self, event):
        bashCommand = f'spotify'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    def open_stream1(self, event):
        bashCommand = f'streamlink twitch.tv/theddy best'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

        

    def open_stream2(self, event):
        bashCommand = f'streamlink twitch.tv/konni best'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    def get_ram(self):
        self.progressBar.setValue(round(psutil.virtual_memory().percent))
        #self.temperaturLabel.setText(str(psutil.sensors_temperatures(
        #    fahrenheit=False)['coretemp'][0][1]) + "°C CPU")

    def check_mail(self):

        imap_host = 'imap.gmail.com'
        imap_user = 'torashelly@gmail.com'
        pw = 'i2Bt3vrCkMLv4AQt'

        # init imap connection
        mail = imaplib.IMAP4_SSL(imap_host, 993)
        rc, resp = mail.login(imap_user, pw)

        # select only unread messages from inbox
        mail.select('Inbox')
        status, data = mail.search(None, '(UNSEEN)')
        i = 0
        # for each e-mail messages, print text content
        for num in data[0].split():
            i = i + 1

        self.mailLabel.setText(f'Sie haben {i} neue Mails')

        

    def check_sprit(self):
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        url = "https://ich-tanke.de/tankstellen/super-e5/region/leipzig/"

        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        durch = soup.find('div', class_='box-ersparnis')
        test = durch.find_next('div', class_='box-ersparnis')
        
        print(test)
        test = str(test)
        x = test.find("Günstig")
        z = x 
        print(test[x:-10])

        self.spritLabel.setText(f'Sprit: {test[x:-10]}')


    def start_Game(self):

        if self.gameCombo.currentText() == "Path of Exile":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 238960")
            
            #subprocess.call(r"C:\Users\Tora\AppData\Local\Programs\Awakened PoE Trade\Awakened PoE Trade.exe")
            
            #subprocess.call(r"C:\Users\Tora\AppData\Local\PoeLurker\PoeLurker.exe")
            
            #subprocess.call(r"C:\Users\Tora\AppData\Roaming\Path of Building Community\Path of Building.exe")
            
            #bashCommand = f'steam steam://rungameid/238960'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)
            #bashCommand = f'PathOfBuildingCommunity %U'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)
            #bashCommand = f'terminator -e ~/trade.sh'
            #process = subprocess.Popen(
                   # bashCommand.split(), stdout=subprocess.PIPE)
            
        if self.gameCombo.currentText() == "Anno 1800":
            bashCommand = f'env LUTRIS_SKIP_INIT=1 lutris lutris:rungameid/4'
            process = subprocess.Popen(
                    bashCommand.split(), stdout=subprocess.PIPE)
        if self.gameCombo.currentText() == "Lost Ark":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 1599340")
            
        if self.gameCombo.currentText() == "Last Epoch":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 899770")
            #bashCommand = f'steam steam://rungameid/899770'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)
        if self.gameCombo.currentText() == "Foundation":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 690830")
            #bashCommand = f'steam steam://rungameid/690830'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)
        if self.gameCombo.currentText() == "Kingdoms Reborn":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 1307890")
            #bashCommand = f'steam steam://rungameid/1307890'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)
        if self.gameCombo.currentText() == "The Universim":
            subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 352720")
            #bashCommand = f'steam steam://rungameid/352720'
            #process = subprocess.Popen(
                    #bashCommand.split(), stdout=subprocess.PIPE)

    def like_song(self):
        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "playlist-read-private user-read-recently-played user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public user-modify-playback-state"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        results = sp.currently_playing('DE')
        id = []
        if results is not None:
            id.append(results['item']['uri'])

        print(id)
        sp.playlist_add_items('2Yp2HRK0ahORVFOHY8NjgJ', id)

    def prev_song(self):
        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "user-read-recently-played user-read-playback-state user-read-currently-playing user-modify-playback-state"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        sp.previous_track()
        results = sp.currently_playing('DE')
        if results is not None:
            artist = results['item']['album']['artists'][0]['name']
            song = results['item']['name']
            self.spotifyLabel.setText(f'{artist} - {song}')
        else:
            self.spotifyLabel.setText("Spotify is not running")

    def skip_song(self):
        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "user-read-recently-played user-read-playback-state user-read-currently-playing user-modify-playback-state"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        sp.next_track()
        results = sp.currently_playing('DE')
        if results is not None:
            artist = results['item']['album']['artists'][0]['name']
            song = results['item']['name']
            self.spotifyLabel.setText(f'{artist} - {song}')
        else:
            self.spotifyLabel.setText("Spotify is not running")

    def get_song(self):
        client_ID = '2c162080a32b4d6eac1f047d7504e9e7'
        client_SECRET = '64e1ad4b780a466f88fd5e28ea79c26b'
        redirect_url = 'http://localhost'

        scope = "user-read-recently-played user-read-playback-state user-read-currently-playing"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scope))

        results = sp.currently_playing('DE')
        if results is not None:
            artist = results['item']['album']['artists'][0]['name']
            song = results['item']['name']
            self.spotifyLabel.setText(f'{artist} - {song}')
        else:
            self.spotifyLabel.setText("Spotify is not running")

    def check_streamer(self):

        test = self.get_streams(111400170)
        if len(test) == 0:
            self.twitchLabel.setText("Theddy is offline")
            self.twitchLabel.setStyleSheet("color: red")
        else:
            title = test[0]['title']
            viewer = test[0]['viewer_count']
            game = test[0]['game_name']
            self.twitchLabel.setText(
                f'Theddy {game} Title: {title} Viewer: {viewer} ')
            self.twitchLabel.setStyleSheet("color: green")

        test = self.get_streams(29101427)
        if len(test) == 0:
            self.twitchLabel_2.setText("Konni is offline")
            self.twitchLabel_2.setStyleSheet("color: red")
        else:
            title = test[0]['title']
            viewer = test[0]['viewer_count']
            game = test[0]['game_name']
            self.twitchLabel_2.setText(
                f'Konni {game} Title: {title} Viewer: {viewer} ')
            self.twitchLabel_2.setStyleSheet("color: green")

    def on_pushButton_clicked(self):
        self.ui.show()

    def start_browser(self):
        QCoreApplication.setOrganizationName("Shalora")
        QCoreApplication.setOrganizationDomain("www.Shalora.com")
        QCoreApplication.setApplicationName("Test Browser")

        w = test.MainWindow()
        w.show()

    def start_bot(self):
        bashCommand = f'terminator -e ~/bot.sh'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    def start_Le(self):
        bashCommand = f'steam steam://rungameid/899770'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    def make_screenshot(self):
        myScreenshot = pyautogui.screenshot()
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'test.png')
        myScreenshot.save(getpath)

        bashCommand = f'krita {getpath}'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def make_video(self):
        output = "video.avi"
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        #get info from img
        height, width, channels = img.shape
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, 10.0, (width, height))

        while(True):
            try:
                img = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(image)
                StopIteration(0.5)
            except KeyboardInterrupt:
                break

        out.release()
        cv2.destroyAllWindows()

    def read_request(self):

        api_key = "468ed8b94ae6a250c39ebe10b13d755e"

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat=51.342&lon=12.375&exclude=minutely,hourly,alerts&appid={api_key}&units=metric&lang=de'

        data = requests.get(url).json()

        temperature = data['current']['temp']
        status = data['current']['weather'][0]['description']
        day_1 = datetime.utcfromtimestamp(
            data['daily'][1]['dt']).strftime('%d-%m-%Y')
        day_1_temp = data['daily'][1]['temp']['day']
        day_1_desc = data['daily'][1]['weather'][0]['description']

        printable = f'Leipzig\n{status}\n{temperature}°C\n\n{day_1}\n{day_1_temp}°C\n{day_1_desc}'

        self.wetterLabel.setText(printable)
        self.wetterLabel.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
