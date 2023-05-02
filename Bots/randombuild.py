import sqlite3
import os
import random
import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'builds.db')
disk_db = sqlite3.connect(getpath)

#builds = ["Armageddon Brand", "Storm Brand",
#"Toxic Rain Champion", "Minions", "Eye of winter"]


#print(builds[random.randint(0, 4)])
def printrandom():
    cursor = disk_db.cursor()
    exucute = f'SELECT * FROM list'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()

    randombuild = random.randint(0, len(zeilen)-1)
    #print(zeilen[randombuild])
    buildreturn = [zeilen[randombuild][1], zeilen[randombuild][2]]
    return buildreturn


def findinbuilds(searchstring):
    links = []
    hrefs = []
    if searchstring != "build" and searchstring != "3.21" and searchstring != "":
        cursor = disk_db.cursor()
        exucute = f'SELECT * FROM list'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        for zeile in zeilen:
            links.append(zeile[1])
            hrefs.append(zeile[2])

        

        i = 0
        returnstrings = []
        for item in links:

            if item.lower().find(searchstring.lower()) != -1:

                if hrefs[i] not in str(returnstrings):
                    returnstrings.append(f"{item} - {hrefs[i]}")
            i += 1

    return returnstrings


#test = title_span.findAll('a')


#print(test[0]['title'])

def dbwriteonline():
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }



    links = []
    hrefs = []

    patch = "3.21"

    league = "Crucible"
    

    cursor = disk_db.cursor()
    cursor.execute(f'delete from list')
    disk_db.commit()

    i = 1

    while i <= 7:
        url = f"https://www.poe-vault.com/guides/builds-for-path-of-exile?page={i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
            
            for title in title_span:

                if title.text:
                    
                    if "Build Guide" in title.text and (patch in title.text):
                        titleins = title.text.strip()
                        
                        href = title.get('href')
                        titleins = titleins.replace('"', '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        print(titleins)
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()



            i += 1
    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/22/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1

    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/40/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1

    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/marauder/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1
   

    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/24/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1
    
    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/436/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1

    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/303/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1

    i = 1
    while i <= 3:
        url = f"https://www.pathofexile.com/forum/view-forum/41/page/{i}"

        if url is not None:
            page = requests.get(url, headers=HEADERS)
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_span = soup.findAll('a')
                
            for title in title_span:
                if title.text:
                    if patch in title.text:
                        titleins = title.text.strip()
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace(league, '')
                        titleins = titleins.replace('"', '')
                        print(titleins)
                        href = 'https://www.pathofexile.com' + title.get('href') 
                        cursor.execute(f'INSERT INTO list ("title", "href") VALUES ("{titleins}", "{href}")')
                        disk_db.commit()
            i += 1

