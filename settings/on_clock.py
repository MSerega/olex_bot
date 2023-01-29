import aioschedule
import asyncio
import handlers
from scripts.horoscope import update_horoscope


async def scheduler():
    aioschedule.every().day.at("09:06").do(update_horoscope)
    aioschedule.every().day.at("7:00").do(handlers.groups.change_permissions.message_permissions_access)
    aioschedule.every().day.at("7:30").do(handlers.channels.morning_pidsluhaho.morning_weather)
    # aioschedule.every().day.at("8:30").do(handlers.channels.morning_pidsluhaho.morning_fuel)
    aioschedule.every().day.at("9:00").do(handlers.channels.morning_pidsluhaho.morning_memory)
    aioschedule.every().day.at("23:00").do(handlers.groups.change_permissions.message_permissions_block)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
