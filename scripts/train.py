import requests
from bs4 import BeautifulSoup
from settings.config import TRAINS


def get_trains():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    response_trains = requests.get(TRAINS, headers=headers)
    response_trains.encoding = 'utf-8'
    soup = BeautifulSoup(response_trains.content, 'lxml')

    table_train = soup.find('div', attrs={'id': 'tabs-trains'})
    rows = [*table_train.findAll('tr', attrs={'class': 'on'}), *table_train.findAll('tr', attrs={'class': 'onx'})[2:]]
    trains = []
    for row in rows:
        col = row.findAll('td')
        number = col[0].a.text
        days = col[1].getText()
        way = col[2].getText()
        time_start = col[3].getText()
        time_end = col[4].getText()
        trains.append({'number': number, 'days': days, 'way': way, 'time_start': time_start, 'time_end': time_end})
    trains.sort(key=lambda d: d['time_start'])
    return trains
