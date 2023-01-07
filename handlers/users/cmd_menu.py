import asyncio
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import InputFile

from settings import functions
import language
import scripts
from loader import dp, bot
from keyboards import default as kb

now = datetime.now() - timedelta(seconds=600)

last_times = {
    'map': {},
    'weather': {},
    'exchange': {},
    'fuel': {},
}


@dp.message_handler(commands=['menu'], state="*")
async def command_menu(message: types.Message):
    await functions.userInDb(message)
    await message.answer("Оберіть функцію ", reply_markup=kb.main_menu, disable_notification=True)


@dp.message_handler(text="🚨 Мапа тривог", state="*")
@dp.message_handler(commands=['map'], state="*")
async def command_map(message: types.Message):
    await functions.userInDb(message)
    if message.chat.type == 'private':
        await message.answer_photo(InputFile("/home/dan/pm2/static_files/map.png"),
                                   caption=f"\U0001F6A8 Карта повітряних тривог - {datetime.now().strftime('%H:%M')}" +
                                           kb.links,
                                   disable_notification=True)
    else:
        last_times['map'].setdefault(message.chat.id, now)
        if (datetime.now() - last_times['map'][message.chat.id]).seconds < 1800:
            mes = await message.answer(language.ua.check_command_spam_map, disable_notification=True)
            asyncio.create_task(functions.delete_message(mes, 10))
            await message.delete()
            return
        await bot.send_photo(message.chat.id, InputFile("/home/dan/pm2/static_files/map.png"),
                             caption=f"\U0001F6A8 Карта повітряних тривог - {datetime.now().strftime('%H:%M')}" +
                                     kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())
        last_times['map'][message.chat.id] = datetime.now()


@dp.message_handler(text="🌤 Погода", state="*")
@dp.message_handler(commands=['weather'], state="*")
async def command_weather(message: types.Message):
    await functions.userInDb(message)
    if message.chat.type == 'private':
        await bot.send_photo(message.chat.id, InputFile("images/weather.jpg"),
                             caption=scripts.weather.get_weather() + kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())
    else:
        last_times['weather'].setdefault(message.chat.id, now)
        if (datetime.now() - last_times['weather'][message.chat.id]).seconds < 600:
            mes = await message.answer(language.ua.check_command_spam_weather, disable_notification=True)
            asyncio.create_task(functions.delete_message(mes, 10))
            await asyncio.sleep(2)
            await message.delete()
            return
        await message.answer(scripts.weather.get_weather() +
                             kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())
        last_times['weather'][message.chat.id] = datetime.now()


@dp.message_handler(text="💵 Курс валют", state="*")
@dp.message_handler(commands=['exchange'], state="*")
async def command_exchange(message: types.Message):
    await functions.userInDb(message)
    if message.chat.type == 'private':
        await message.answer(scripts.exchange.get_exchange() +
                             kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())
    else:
        last_times['exchange'].setdefault(message.chat.id, now)
        if (datetime.now() - last_times['exchange'][message.chat.id]).seconds < 600:
            mes = await message.answer(language.ua.check_command_spam_exchange, disable_notification=True)
            asyncio.create_task(functions.delete_message(mes, 10))
            await asyncio.sleep(2)
            await message.delete()
            return
        await message.answer(scripts.exchange.get_exchange() + kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())
        last_times['exchange'][message.chat.id] = datetime.now()

# @dp.message_handler(commands=['fuel'], state="*")
# async def command_fuel(message: types.Message):
#     if message.chat.type == 'private':
#         load = await message.answer(language.ua.load_fuel_information, disable_notification=True)
#         asyncio.create_task(functions.delete_message(load, 4))
#         await message.answer(scripts.fuel.get_fuel(), disable_notification=True, disable_web_page_preview=True)
#     else:
#         last_times['fuel'].setdefault(message.chat.id, now)
#         if (datetime.now() - last_times['fuel'][message.chat.id]).seconds < 600:
#             mes = await message.answer(language.ua.check_command_spam_fuel, disable_notification=True)
#             asyncio.create_task(functions.delete_message(mes, 5))
#             await asyncio.sleep(2)
#             await message.delete()
#             return
#         load = await message.answer(language.ua.load_fuel_information, disable_notification=True)
#         asyncio.create_task(functions.delete_message(load, 4))
#         await message.answer(scripts.fuel.get_fuel(), disable_notification=True, disable_web_page_preview=True)
#         last_times['fuel'][message.chat.id] = datetime.now()
