import aioschedule
import asyncio
import handlers
from scripts.horoscope import update_horoscope
from scripts.news_rss import generalised_parse


async def scheduler():
    aioschedule.every().day.at("00:00").do(update_horoscope)
    # aioschedule.every().day.at("7:00").do(handlers.groups.change_permissions.message_permissions_access)
    aioschedule.every().day.at("7:30").do(handlers.channels.morning_pidsluhaho.morning_weather)
    # aioschedule.every().day.at("8:30").do(handlers.channels.morning_pidsluhaho.morning_fuel)
    aioschedule.every().day.at("9:00").do(handlers.channels.morning_pidsluhaho.morning_memory)
    # aioschedule.every().day.at("23:00").do(handlers.groups.change_permissions.message_permissions_block)
    # for hour in range(7, 24):
    #     aioschedule.every().day.at(f"{hour}:00").do(generalised_parse)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
