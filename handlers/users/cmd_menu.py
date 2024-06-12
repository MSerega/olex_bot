import asyncio
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.exceptions import Throttled

from settings import functions
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


@dp.message_handler(commands=['menu'], chat_type=types.ChatType.PRIVATE, state="*")
async def command_menu(message: types.Message):
    try:
        await dp.throttle('menu', rate=2)
    except Throttled:
        await message.reply('Забагато запитів, спробуйте через 2 секунд.')
    else:
        await functions.userInDb(message)
        await message.answer("Оберіть функцію ", reply_markup=kb.main_menu, disable_notification=True)


@dp.message_handler(text="🚨 Мапа тривог", state="*", chat_type=types.ChatType.PRIVATE)
@dp.message_handler(commands=['map'], state="*", chat_type=types.ChatType.PRIVATE)
async def command_map(message: types.Message):
    try:
        await dp.throttle('map', rate=2)
    except Throttled:
        await message.reply('Забагато запитів, спробуйте через 2 секунд.')
    else:
        await functions.userInDb(message)
        await message.answer_photo(InputFile("/var/www/alerts_map.png"),
                                   caption=f"\U0001F6A8 Карта повітряних тривог - "
                                           f"{datetime.now().strftime('%H:%M')}" + kb.links,
                                   disable_notification=True)


@dp.message_handler(text="🌤 Погода", state="*", chat_type=types.ChatType.PRIVATE)
@dp.message_handler(commands=['weather'], state="*", chat_type=types.ChatType.PRIVATE)
async def command_weather(message: types.Message):
    try:
        await dp.throttle('weather', rate=2)
    except Throttled:
        await message.reply('Забагато запитів, спробуйте через 2 секунд.')
    else:
        await functions.userInDb(message)
        await bot.send_message(message.chat.id, text=scripts.weather.get_weather() + kb.links,
                               disable_web_page_preview=True, disable_notification=True, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="💵 Курс валют", state="*", chat_type=types.ChatType.PRIVATE)
@dp.message_handler(commands=['exchange'], state="*", chat_type=types.ChatType.PRIVATE)
async def command_exchange(message: types.Message):
    try:
        await dp.throttle('exchange', rate=2)
    except Throttled:
        await message.reply('Забагато запитів, спробуйте через 2 секунд.')
    else:
        await functions.userInDb(message)
        await message.answer(scripts.exchange.get_exchange() + kb.links,
                             disable_notification=True, reply_markup=types.ReplyKeyboardRemove())

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
