import requests
import re
import smtplib
import json
import os
import sqlite3
import time
import playsound

from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

MAIL_ADDRESS = 'torashelly@gmail.com'
PASSWORD = 'i2Bt3vrCkMLv4AQt'

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'articles.json')
ARTICLE_FILE = getpath


def read_json():
    articles = []
    try:
        with open(ARTICLE_FILE, 'r') as file:
            articles = json.load(file)
    except FileNotFoundError as e:
        print(ARTICLE_FILE, 'does not exist')

    except json.decoder.JSONDecodeError as e:
        print('Invalid json file:', e.msg, 'in line', e.lineno)

    return articles


def validate_articles(articles):
    valid_articles = []
    for article in articles:
        if ('url' not in article or 'target_price' not in article):
            continue

        if ('amazon.de' not in article['url'] or type(article['target_price'])
                is not float):
            continue

        valid_articles.append(article)

    return valid_articles


def parse_price(price_text):

    price_text = price_text.replace('€', '')
    price_text = price_text.replace('EUR', '')
    price_text = price_text.strip()
    price_text = price_text.replace('.', '')
    price_text = price_text.replace(',', '.')

    return float(price_text)


def get_article_details(article):
    url = article['url']

    article['price'] = 0.0
    article['name'] = ''
    if url is not None:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        title_span = soup.find('span', id='productTitle')
        if title_span is not None:
            article['name'] = title_span.get_text().strip()

        price_span = soup.find('span', id='priceblock_dealprice')

        if price_span is None:
            price_span = soup.find('span', id='priceblock_ourprice')

        if price_span is None:
            price_span = soup.find('span', class_='a - color - price')

        if price_span is None:
            price_span = soup.find('span', class_='a-offscreen')

        if price_span is not None:

            article['price'] = parse_price(price_span.get_text())

    return article


def send_email(article_details):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(MAIL_ADDRESS, PASSWORD)

    subject = f"{article_details['name']} price below {article_details['target_price']} €"
    body = f"The article {article_details['name']} is available for {article_details['price']} €. Check it here: {article_details['url']}"

    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(MAIL_ADDRESS, MAIL_ADDRESS, message.encode('utf8'))
    server.quit()


def amazonread(self):
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    getpath = os.path.join(bundle_dir, 'preise.db')
    disk_db = sqlite3.connect(getpath)
    cursor = disk_db.cursor()

    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%d.%m.%Y %H:%M:%S", named_tuple)

    articles = read_json()
    valid_articles = validate_articles(articles)

    for article in valid_articles:

        article_details = get_article_details(article)
        print(f'{article_details["name"]} - {article_details["price"]}')
        produktname = article_details["name"]
        produktpreis = article_details["price"]
        if article_details['price'] > 0.0:
            exucute = f'INSERT INTO preisverlauf ("datum", "produkt", "preis") VALUES ("{time_string}", "{produktname}", "{produktpreis}")'
            cursor.execute(exucute)
            disk_db.commit()
            #if article_details['price'] < 17:
                #playsound('horn.mp3')
            if produktname == "LEGO 76389 Harry Potter Schloss Hogwarts Kammer des Schreckens Spielzeug, Set mit Voldemort als goldene Minifigur und der Großen Halle":

                self.tinaLabel.setText(f'Geschenk: {produktpreis}')
        if (article_details['price'] is not None
                and article_details['price'] <= article['target_price']) and article_details['price'] > 0.0:
            #send_email(article_details)
            print("")


