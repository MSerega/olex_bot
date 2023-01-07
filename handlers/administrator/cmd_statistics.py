from aiogram import types
from loader import dp

from db.db_connect import get_users
from settings.config import ADMIN


@dp.message_handler(commands=['statistics'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def command_start(message: types.Message):
    users = len(get_users())
    await message.answer(f"👩‍👧‍👦 Всього в базі: {users} людей.", disable_notification=True)
