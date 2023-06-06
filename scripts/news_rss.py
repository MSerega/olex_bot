import asyncio
import re
import ssl
import requests

import feedparser
from loader import bot
from db.db_connect import check_rss_news_exists, add_rss_news
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import default as kb
from settings.config import c_pidsluhano_id

ssl._create_default_https_context = ssl._create_unverified_context


async def generalised_parse():
    feed_urls = [
        {"url": "https://tsn.ua/rss/full.rss", "description": "Свіжі новини TCН"},
        {"url": "https://oleks-selrada.gov.ua/category/news/feed/",
         "description": "Новини Олександрівської територіальної громади"}
    ]

    newsInfo = []

    for feed in feed_urls:
        feed_url = feed["url"]
        feed_description = feed["description"]

        response = requests.get(feed_url)
        raw = response.text
        raw = re.sub(r'(<item>.*?)<image>.*?(http.*?jpg|png|gif).*?</image>(.*?</item>)',
                     r'\1<enclosure url="\2" />\3', raw)

        if raw:
            parser = feedparser.parse(raw)
        else:
            parser = feedparser.parse(feed_url)

        if parser.entries:
            latest_entry = parser.entries[0]

            if latest_entry.enclosures:
                enclosure_href = latest_entry.enclosures[0]['href']
            else:
                enclosure_href = ''

            newEntry = {
                'title': latest_entry.get('title', ''),
                'description': latest_entry.get('summary', ''),
                'link': latest_entry.get('link', ''),
                'image': enclosure_href,
                'source_description': feed_description,
                'source': feed_url
            }
            newsInfo.append(newEntry)

            if not check_rss_news_exists(newEntry["source"], newEntry["title"]):
                link_button = InlineKeyboardMarkup().row(
                    InlineKeyboardButton("📢 Дізнатися більше", url=newEntry["link"]))

                message = f"💬 {newEntry['source_description']}:\n\n<b>{newEntry['title']}{kb.links}</b>"

                if latest_entry.enclosures:
                    await bot.send_photo(c_pidsluhano_id, newEntry['image'], caption=message, reply_markup=link_button)
                else:
                    await bot.send_message(c_pidsluhano_id, message, reply_markup=link_button)

                add_rss_news(feed_url, newEntry["title"], newEntry["link"])
                await asyncio.sleep(1500)
    return newsInfo


async def rss_start():
    while True:
        await generalised_parse()
