import asyncio
from aiogram import types
from loader import dp
import subprocess

from settings.config import ADMIN


@dp.message_handler(commands=['reboot_olex_bot'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def command_start(message: types.Message):
    try:
        await message.answer(f"Перезавантаження бота", disable_notification=True)
        subprocess.call(["pm2", "restart", "0"])
    except subprocess.CalledProcessError:
        await message.answer(f"Сталась помилка перезавантаження", disable_notification=True)


@dp.message_handler(commands=['reboot_alarm_bot'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def command_start(message: types.Message):
    try:
        await message.answer(f"Перезавантаження бота", disable_notification=True)
        subprocess.call(["pm2", "restart", "1"])
    except subprocess.CalledProcessError:
        await message.answer(f"Сталась помилка перезавантаження", disable_notification=True)
