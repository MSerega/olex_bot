from aiogram import types
from loader import dp
from scripts.horoscope import update_horoscope
from settings.config import ADMIN


@dp.message_handler(commands=['update_horoscope'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def update_admin_horoscope(message: types.Message):
    await update_horoscope()
    await message.answer("Оновлення завершено.")