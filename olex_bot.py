from aiogram import executor, types

from db.db_connect import insert_db_horoscope
from loader import dp

from db import db_connect
import asyncio


import middlewares, filters, handlers
from scripts.horoscope import update_horoscope
from settings import bot_commands, on_clock

from datetime import datetime


async def on_startup(dp):
    await db_connect.database()
    asyncio.create_task(on_clock.scheduler())
    await bot_commands.set_commands(dp)
    print(f'{datetime.now()} Bot Started')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
