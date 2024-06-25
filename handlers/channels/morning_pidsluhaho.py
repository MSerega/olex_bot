from aiogram.types import InputFile

from loader import bot
from scripts import weather
from settings.config import c_pidsluhano_id
from keyboards.default import links


async def morning_weather():
    # await bot.send_photo(c_pidsluhano_id, InputFile("images/weather.jpg"), caption=weather.get_weather() + links,
    # disable_notification=True)
    await bot.send_message(c_pidsluhano_id, weather.get_weather() + links, disable_notification=True)


async def morning_memory():
    await bot.send_photo(c_pidsluhano_id, InputFile("images/memory.jpg"))
