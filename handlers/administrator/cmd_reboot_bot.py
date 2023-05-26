from aiogram import types
from loader import dp
import subprocess

from settings.config import ADMIN


@dp.message_handler(commands=['reboot_bot'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def command_start(message: types.Message):
    try:
        subprocess.call(["pm2", "restart", "0"])
        await message.answer(f"Перезавантаження бота", disable_notification=True)
    except:
        await message.answer(f"Сталась помилка перезавантаження", disable_notification=True)
