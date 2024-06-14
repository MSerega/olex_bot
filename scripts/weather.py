from datetime import datetime

import requests
from bs4 import BeautifulSoup

from settings.config import SINOPTIK


def get_weather():
    # сторінки з яких буде проводитись парсинг
    url_sinoptik = SINOPTIK

    # Заголовки необхідні для доступу до деяких сайтів
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    # Витягуємо html код сторінок
    response_sinoptik = requests.get(url_sinoptik, headers=headers)
    soup_sinoptik = BeautifulSoup(response_sinoptik.content, 'lxml')

    # Створення словників для відповідності англійських та українських назв днів тижня та місяців
    uk_weekdays = {
        'Monday': 'Понеділок',
        'Tuesday': 'Вівторок',
        'Wednesday': 'Середа',
        'Thursday': 'Четвер',
        'Friday': 'П\'ятниця',
        'Saturday': 'Субота',
        'Sunday': 'Неділя'
    }

    uk_months = {
        'January': 'січня',
        'February': 'лютого',
        'March': 'березня',
        'April': 'квітня',
        'May': 'травня',
        'June': 'червня',
        'July': 'липня',
        'August': 'серпня',
        'September': 'вересня',
        'October': 'жовтня',
        'November': 'листопада',
        'December': 'грудня'
    }

    current_date = datetime.now()
    weekday_name = current_date.strftime("%A")
    month_name = current_date.strftime("%B")
    uk_weekday_name = uk_weekdays.get(weekday_name, weekday_name)
    uk_month_name = uk_months.get(month_name, month_name)
    today_date = f"{current_date.day} {uk_month_name} {current_date.year} року"

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

    # Парсимо cхід та захід сонця
    time_weather = soup_sinoptik.find('div', class_='infoDaylight').text
    time_tokens = time_weather.split()
    sunrise_time = time_tokens[1]
    sunset_time = time_tokens[3]

    # Парсимо часу заходу і сходу сонця
    times_day = []
    for item in soup_sinoptik.select('.infoDaylight > span'):
        times_day += item

    weather_table = soup_sinoptik.select_one('.weatherDetails')

    if weather_table:
        rows = weather_table.select('tbody tr')

        if rows:
            # Парсинг часу, температури, відчуття як, тиску, вологості, вітру та ймовірності опадів
            times = [td.get_text(strip=True) for td in rows[0].select('td')]
            weather_descriptions = [td.find('div')['title'] for td in rows[1].select('td')]
            temperatures = [td.get_text(strip=True) for td in rows[2].select('td')]
            feels_like = [td.get_text(strip=True) for td in rows[3].select('td')]
            pressures = [td.get_text(strip=True) for td in rows[4].select('td')]
            humidity = [td.get_text(strip=True) for td in rows[5].select('td')]
            winds = [td.get_text(strip=True) for td in rows[6].select('td')]
            precipitation_chances = [td.get_text(strip=True) if td.get_text(strip=True) != '-' else '0' for td in rows[7].select('td')]


            # Формування текстового результату
            result = (f"📅 {uk_weekday_name} {today_date} \n"
                      f"{desc}\n\n"
                      "Детальна інформація про погоду\n"
                      f"🌅 Cхід сонця: {sunrise_time}\n"
                      f"🌄 Захід сонця: {sunset_time}\n\n"
                      + "\n".join(['-' * 50 +
                                   f"\n🕝 Час: {times[i]}\n"
                                   f"🗾 На небі: {weather_descriptions[i]}\n"
                                   f"🌡 Температура: {temperatures[i]} °C\n"
                                   f"🌡 Відчувається як: {feels_like[i]}\n"
                                   f"🌏 Тиск: {pressures[i]} мм.\n"
                                   f"💧 Вологість: {humidity[i]}%\n"
                                   f"🌁 Вітер: {winds[i]} м/сек\n"
                                   f"🌨 Ймовірність опадів: {precipitation_chances[i]} %"
                                   for i in range(len(times))]))

            print(result)
            return result
        else:
            return "Не вдалося знайти рядки таблиці."
    else:
        return "Не вдалося знайти таблицю weatherDetails."
