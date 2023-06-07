from aiogram import executor
from loader import dp
from db import db_connect
import asyncio

import middlewares, filters, handlers
from settings import bot_commands, on_clock
from datetime import datetime


async def on_startup(dp):
    await db_connect.database()
    asyncio.create_task(on_clock.scheduler())
    await bot_commands.set_commands(dp)
    print(f"{datetime.now().strftime('%H:%M')} Bot started!")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
