# importing libraries
import requests
import re
import os
import sqlite3
import time
from bs4 import BeautifulSoup

  
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

url = "https://ich-tanke.de/tankstellen/super-e5/region/leipzig/"

page = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(page.content, 'html.parser')
durch = soup.find('div', class_='box-ersparnis')
test = durch.find_next('div', class_='box-ersparnis')


test = str(test)
x = test.find("Günstig")
z = x 


#self.spritLabel.setText(f'Sprit: {test[x:-10]}')
longs = test[x:-10]
mittel = longs[26:30]


print(mittel)

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'sprit.db')
disk_db = sqlite3.connect(getpath)
cursor = disk_db.cursor()

named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%d.%m.%Y %H:%M:%S", named_tuple)

exucute = f'INSERT INTO preise ("datum", "preis") VALUES ("{time_string}", "{mittel}")'
cursor.execute(exucute)
disk_db.commit()