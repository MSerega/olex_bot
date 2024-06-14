import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
import asyncio

from keyboards.default import links
from loader import bot
from settings.config import OLEX_NEWS, c_pidsluhano_id
from db.db_connect import check_news_exists, add_news


async def get_news():
    # сторінки з яких буде проводитись парсинг
    url_olex_news = OLEX_NEWS

    # Заголовки необхідні для доступу до деяких сайтів
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    # Витягуємо html код сторінок
    response_olex_news = requests.get(url_olex_news, headers=headers)
    soup_olex_news = BeautifulSoup(response_olex_news.content, 'lxml')

    link = soup_olex_news.find('h2', class_='entry-title').a['href']
    title = soup_olex_news.find('h2', class_='entry-title').text.strip()
    description = soup_olex_news.find('div', class_='entry-summary').p.get_text(strip=True)
    image_src = soup_olex_news.find('div', class_='entry-featuredImg').img['src']

    link_button = InlineKeyboardMarkup().row(
        InlineKeyboardButton("📢 Дізнатися більше", url=link))

    if not check_news_exists(link, title):
        add_news(url_olex_news, link, title, image_src)
        await bot.send_photo(145333452, image_src, caption=f"💬 Новини Олександрівської територіальної громади:\n\n<b>{title}</b>\n" + links, reply_markup=link_button)
    else:
        print(f"Новина '{title}' вже існує в базі даних")


