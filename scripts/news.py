import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from bs4 import BeautifulSoup
import asyncio

from keyboards.default import links
from loader import bot
from settings.config import OLEX_NEWS, c_pidsluhano_id
from db.db_connect import check_news_exists, add_news


async def get_news():
    # Сторінка з якої буде проводитись парсинг
    url_olex_news = "OLEX_NEWS_URL"

    # Заголовки необхідні для доступу до деяких сайтів
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

    # Витягуємо html код сторінок
    response_olex_news = requests.get(url_olex_news, headers=headers)
    soup_olex_news = BeautifulSoup(response_olex_news.content, 'lxml')

    # Отримуємо всі статті на сторінці
    articles = soup_olex_news.find_all('article')

    for article in articles:
        link = article.find('h2', class_='entry-title').a['href']
        title = article.find('h2', class_='entry-title').text.strip()
        description = article.find('div', class_='entry-summary').p.get_text(strip=True)

        # Перевірка наявності зображення
        img_tag = article.find('div', class_='entry-featuredImg')
        if img_tag and img_tag.img:
            image_src = img_tag.img['src']
        else:
            # Вставка власної картинки, якщо зображення відсутнє
            image_src = 'images/notnews.jpg'

        link_button = InlineKeyboardMarkup().row(
            InlineKeyboardButton("📢 Дізнатися більше", url=link))

        if not check_news_exists(link, title):
            add_news(url_olex_news, link, title, image_src)
            if image_src.startswith('http'):
                await bot.send_photo(c_pidsluhano_id, image_src,
                                     caption=f"💬 Новини Олександрівської територіальної громади:\n<b>{title}</b>" + links,
                                     reply_markup=link_button)
            else:
                await bot.send_photo(c_pidsluhano_id, InputFile(image_src),
                                     caption=f"💬 Новини Олександрівської територіальної громади:\n<b>{title}</b>" + links,
                                     reply_markup=link_button)


