import asyncio
import ssl

import feedparser
from loader import bot
from db.db_connect import check_rss_news_exists, add_rss_news
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ssl._create_default_https_context = ssl._create_unverified_context


async def check_news_and_publish():
    feed_urls = [
        {"url": "https://tsn.ua/rss/full.rss", "source": "2", "description": "Свіжі новини TCН"},
        {"url": "https://oleks-selrada.gov.ua/category/news/feed/", "source": "1",
         "description": "Новини Олександрівської територіальної громади"}
    ]
    for feed_data in feed_urls:
        feed_url = feed_data["url"]
        feed_source_description = feed_data["description"]
        feed_source = feed_data["source"]

        feed = feedparser.parse(feed_url)
        if 'entries' in feed and len(feed.entries) > 0:
            latest_entry = feed.entries[0]
            news_title = latest_entry.title
            news_link = latest_entry.link

            if not check_rss_news_exists(feed_url, news_title):
                link_button = InlineKeyboardMarkup().row(
                    InlineKeyboardButton("📢 Дізнатися більше", url=news_link))

                message = f"💬 {feed_source_description}:\n\n<b>{news_title}</b>"
                await bot.send_message(-1001636677869, message, reply_markup=link_button)
                add_rss_news(feed_url, news_title, news_link)
        await asyncio.sleep(1500)


async def rss_start():
    while True:
        await check_news_and_publish()
