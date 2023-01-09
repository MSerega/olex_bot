from aiogram import types
from aiogram.types import InputFile

from loader import dp
from settings.config import ADMIN
import keyboards as kb


@dp.message_handler(commands=["light"], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def cmd_light(message: types.Message):
    if message.text is not None:
        text_from_bot = message.text.split("/light ")
        text_light = text_from_bot[1]
        await dp.bot.send_photo(-1001636677869, InputFile("/home/mserega/bots/olex_bot/images/light.jpg"),
                                caption=text_light, reply_markup=kb.inline.light)
