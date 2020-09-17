import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://alfabank.ru/'
PIC_HOST = 'https:'
URL = 'https://alfabank.ru/everyday/debit-cards/?rp-tab=all'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/85.0.4183.102 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    cards = []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='a-zshM3 f-zshM3 Y1K0FzQ')
    for item in items:
        cards.append(
            {
                'card_name': item.find('a', class_='a1BHA0u g1BHA0u c1BHA0u').get_text(strip=True),
                'card_link': HOST + item.find('a', class_='a1BHA0u g1BHA0u c1BHA0u').attrs['href'],
                'card_picture': PIC_HOST + str(
                    item.find('a', class_='a1BHA0u g1BHA0u e1BHA0u').find('img').get('data-src')),
                'main_description': item.find('p', class_='a31SCNC d31SCNC J31SCNC k31SCNC').get_text(strip=True)
            }
        )
    return cards


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        items = get_content(html.text)
        save_doc(items, 'cards.csv')
    else:
        print('Error')


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Card name', 'Card Link', 'Description', 'Picture Link'])
        for item in items:
            writer.writerow([item['card_name'], item['card_link'], item['main_description'], item['card_picture']])


parse()
