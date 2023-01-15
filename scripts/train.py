from pprint import pprint

import requests
from bs4 import BeautifulSoup
from settings.config import SUBURNAN_TRAINS, PASSENGER_TRAINS


def get_suburnan_trains():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    response_trains = requests.get(SUBURNAN_TRAINS, headers=headers)
    response_trains.encoding = 'utf-8'
    soup = BeautifulSoup(response_trains.content, 'lxml')

    table_train = soup.find('table', attrs={'class': 'schedule_table'})
    rows = table_train.findAll('tr')[1:]
    trains = []
    for row in rows:
        col = row.findAll('td')[1:-1]
        number = col[0].a.text
        way = col[1].getText().strip().replace("\n", "").replace("  ", "").replace("→", "- ")
        time_start = col[2].getText().strip().replace(".", ":")
        time_stop = col[3].getText().strip()
        time_end = col[4].getText().strip().replace(".", ":")
        days = f"<a href='https://poizdato.net{col[5].find('a').attrs['href']}'>{col[5].find('img').attrs['alt'].replace(' - переглянути', '')}</a>"
        trains.append({'number': number, 'days': days, 'way': way, 'time_start': time_start, 'time_stop': time_stop,
                       'time_end': time_end})
    trains.sort(key=lambda d: d['time_start'])
    return trains


def get_passenger_trains():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    response_trains = requests.get(PASSENGER_TRAINS, headers=headers)
    response_trains.encoding = 'utf-8'
    soup = BeautifulSoup(response_trains.content, 'lxml')

    table_train = soup.find('table', attrs={'class': 'schedule_table'})
    rows = table_train.findAll('tr')[1:]
    trains = []
    for row in rows:
        col = row.findAll('td')[1:-1]
        number = col[0].a.text
        way = col[1].getText().strip().replace("\n", "").replace("  ", "").replace("→", "- ")
        time_start = col[2].getText().strip().replace(".", ":")
        time_stop = col[3].getText().strip()
        time_end = col[4].getText().strip().replace(".", ":")
        days = f"<a href='https://poizdato.net{col[5].find('a').attrs['href']}'>{col[5].find('img').attrs['alt'].replace(' - переглянути', '')}</a>"
        trains.append({'number': number, 'days': days, 'way': way, 'time_start': time_start, 'time_stop': time_stop,
                       'time_end': time_end})
    trains.sort(key=lambda d: d['time_start'])
    return trains


