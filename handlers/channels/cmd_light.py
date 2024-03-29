from aiogram import types
from aiogram.types import InputFile

from loader import dp
from settings.config import ADMIN
import keyboards as kb
from settings.config import c_pidsluhano_id


@dp.message_handler(commands=["light"], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def cmd_light(message: types.Message):
    if message.text is not None:
        text_from_bot = message.text.split("/light ")
        text_light = text_from_bot[1]
        await dp.bot.send_photo(c_pidsluhano_id, InputFile("/home/mserega/bots/olex_bot/images/light.jpg"),
                                caption=text_light, reply_markup=kb.inline.light)


@dp.message_handler(commands=["light2"], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def cmd_light(message: types.Message):
    if message.text is not None:
        text_from_bot = message.text.split("/light2 ")
        text_light = text_from_bot[1]
        await dp.bot.send_message(c_pidsluhano_id, text_light, reply_markup=kb.inline.light)
