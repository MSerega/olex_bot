from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp
from keyboards import default as kb
from .states_services import FSM_services

import requests
from bs4 import BeautifulSoup

from settings.config import PASSPORT_TABLE_URL


@dp.message_handler(Text(equals="🧧 Паспортний стіл"), state=FSM_services.services)
async def cmd_passport_table(message: types.Message, state: FSMContext):
    await FSM_services.passport_table.set()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }
    response_horoscope = requests.get(PASSPORT_TABLE_URL, headers=headers)
    response_horoscope.encoding = 'utf-8'
    soup = BeautifulSoup(response_horoscope.content, 'lxml')

    horoscope_content = soup.find('div', attrs={'id': 'collapse16'})

    if horoscope_content:
        mobile_12 = horoscope_content.find(class_="mobile-12")
        if mobile_12:
            mobile_12_text = "\n".join([p.get_text() for p in mobile_12.find_all("p")])
            mobile_12_text = mobile_12_text.replace("Телефон: (05242) 3-28-14", "Телефон: +38(05242)3-28-14")
        else:
            mobile_12_text = ""

        schedule_table = horoscope_content.find("table")
        if schedule_table:
            schedule_rows = schedule_table.find_all("tr")

            schedule_data = []
            for row in schedule_rows:
                columns = row.find_all("td")
                row_data = [column.get_text(strip=True) for column in columns]
                schedule_data.append(row_data)
            schedule_data.pop(0)

            work_graffic = ''
            for i, row_data in enumerate(schedule_data):
                work_graffic += "🕰 " + row_data[0] + ": "
                work_graffic += row_data[1] + " "

                if i != 0 and i != len(schedule_data) - 1:
                    work_graffic += "\n🍽 Обідня перерва: " + row_data[2]

                work_graffic += "\n\n"
        else:
            work_graffic = ""

        message_text = "<b>Олександрівський районний сектор управління державної міграційної служби України у Кіровоградській області</b>\n\n"\
                       f"{mobile_12_text}\n\n"\
                       f"<b>Графік роботи:</b>\n\n"\
                       f"{work_graffic}"

        await message.answer(message_text)
    else:
        await message.answer("Не вдалося знайти необхідну інформацію. Cпробуйте ще раз")
