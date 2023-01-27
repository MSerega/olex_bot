import requests
from bs4 import BeautifulSoup

from db.db_connect import update_db_horoscope,insert_db_horoscope
from settings.config import HOROSCOPE


def update_horoscope():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    for i in range(1, 13):
        response_horoscope = requests.get(HOROSCOPE + str(i), headers=headers)
        response_horoscope.encoding = 'utf-8'
        soup = BeautifulSoup(response_horoscope.content, 'lxml')
        horoscope_content = soup.find('div', attrs={'class': 'horoscope_content'})
        zodiac = horoscope_content.find('h1').text
        prevision = horoscope_content.find('div', attrs={'class': 'column1'}).text
        update_db_horoscope(zodiac, prevision)
