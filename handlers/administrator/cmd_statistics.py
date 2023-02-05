from aiogram import types
from loader import dp

from db.db_connect import get_users, get_count_insurence
from settings.config import ADMIN


@dp.message_handler(commands=['statistics'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def command_start(message: types.Message):
    users = len(get_users())
    insurence = get_count_insurence()
    await message.answer(f"👩‍👧‍👦 Всього в базі: {users} людей.\n"
                         f"🚘 Всього заявок на страхування: {insurence} шт.",

                         disable_notification=True)
