import requests
from bs4 import BeautifulSoup
from settings.config import SINOPTIK, GISMETIO


def get_weather():
    # сторінки з яких буде проводитись парсинг
    url_sinoptik = SINOPTIK
    url_gismetio = GISMETIO

    # Заголовки необхідні для доступу до деяких сайтів
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    # Витягуємо html код сторінок
    response_sinoptik = requests.get(url_sinoptik, headers=headers)
    response_gismetio = requests.get(url_gismetio, headers=headers)

    response_gismetio.encoding = 'utf-8'
    soup_sinoptik = BeautifulSoup(response_sinoptik.content, 'lxml')
    soup_gismetio = BeautifulSoup(response_gismetio.content, 'lxml')

    # Парсимо сайти по їх класах

    # Парсимо опис погоди

    description = [item.text.strip() for item in soup_sinoptik.find_all('div', class_='description')]
    if len(description) == 4:
        desc = description[2]
        people_weather = description[3].replace('Народний прогноз погоди: ', '')
    elif len(description) == 3:
        desc = description[1]
        people_weather = description[2].replace('Народний прогноз погоди: ', '')
    else:
        desc = description[0]
        people_weather = description[1].replace('Народний прогноз погоди: ', '')

    # Парсимо день та час погоди
    day_name = soup_sinoptik.find('p', class_='day-link').text
    time_weather = soup_gismetio.find('div', class_='now-localdate').text
    time_day = time_weather.split(", ")

    # Парсимо температуру в градусах цельсія
    temperatura = soup_gismetio.find('div', class_='now-weather').text.split()

    # Парсимо температуру на відчуття
    vidchuttya = soup_gismetio.find('div', class_='now-feel').text.split()

    # Парсимо погоду на вулиці
    in_street = soup_gismetio.find('div', class_='now-desc').text.strip()

    # Парсимо часу заходу і сходу сонця
    times = []
    for item in soup_sinoptik.select('.infoDaylight > span'):
        times += item

    # Парсимо вітер
    winter_div = soup_gismetio.find('div', class_='unit_wind_m_s')
    winter_unit = []
    for item in winter_div.select('.item-measure > div'):
        winter_unit += item
    winter_div = winter_div.text.split(winter_unit[0])
    winter_div[0] = winter_div[0].strip()

    # Парсимо тиск
    tusk_div = soup_gismetio.find('div', class_='unit_pressure_mm_hg_atm')
    tusk_unit = []
    for item in tusk_div.select('.item-measure > div'):
        tusk_unit += item
    tusk_div = tusk_div.text.split(tusk_unit[0])
    tusk_div[0] = tusk_div[0].strip()

    # Парсимо вологість
    vologist_div = soup_gismetio.find('div', class_='now-info-item humidity')
    vologist = []
    for item in vologist_div:
        vologist += item

    soup_sinoptik.clear()
    soup_gismetio.clear()
    return (
        f"\U0001F4C5 {day_name} {time_day[1]} \U0001F55D {time_day[2]}\n"
        f"{desc}\n\n\U0001F305 "
        f"Схід сонця о: {times[0]}\n\U0001F304 "
        f"Захід сонця о: {times[1]}\n\n"
        f"На даний момент:\n\U0001F321 "
        f"Температура: {temperatura[0]}\n\U0001F321 "
        f"Відчувається як: {vidchuttya[1]}\n\n\U0001F301 "
        f"На вулиці: {in_street}\n\n\U0001F38F "
        f"Вітер: {winter_div[0]} {winter_unit[0]} {winter_unit[1]}\n\U0001F30F "
        f"Тиск:  {tusk_div[0]} {tusk_unit[0]} {tusk_unit[1]}\n\U0001F4A7 "
        f"Вологість: {vologist[1].text} {vologist[2].text}\n\n\n"
        f"🌤 Народний прогноз:\n{people_weather}")
