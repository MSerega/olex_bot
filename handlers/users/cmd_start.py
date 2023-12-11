import asyncio
from aiogram import types

from handlers.users.cmd_advertising import advertising
from handlers.users.cmd_transport import cmd_bus, cmd_taxi
from loader import dp
from keyboards import default as kb
from handlers.users.cmd_news import command_news
from settings.functions import userInDb


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE, state="*")
async def command_start(message: types.Message):
    await userInDb(message)

    arguments = message.get_args()
    if not arguments:
        await message.answer("Вітаю, на даний момент можу вам запропонувати обрати наступні функції:",
                             reply_markup=kb.main_menu, disable_notification=True)
    elif arguments == 'news':
        await command_news(message)
    elif arguments == 'advertising':
        await advertising(message)
    elif arguments == 'bus':
        await cmd_bus(message, "*")
    elif arguments == 'taxi':
        await cmd_taxi(message, "*")
