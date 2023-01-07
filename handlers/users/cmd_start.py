import asyncio
from aiogram import types

from handlers.users.cmd_advertising import advertising
from loader import dp
from keyboards import default as kb
from handlers.users.cmd_news import command_news
from settings.functions import userInDb


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE, state="*")
async def command_start(message: types.Message):
    await userInDb(message)

    arguments = message.get_args()
    if not arguments:
        await message.answer(
            f"Вітаю, на даний момент можу вам запропонувати:"
            f"\n- карту повітряних тривог;"
            f"\n- прогноз погоди в Олександрівці;"
            f"\n- курс валют;"
            f"\n- каталог послуг таксі;"
            f"\n- розклад руху автобусів."
            f"\n- нова пошта (відділення).",
            disable_notification=True)
        await asyncio.sleep(1)
        await message.answer("Оберіть функцію ", reply_markup=kb.main_menu, disable_notification=True)
    elif arguments == 'news':
        await command_news(message)
    elif arguments == 'advertising':
        await advertising(message)
