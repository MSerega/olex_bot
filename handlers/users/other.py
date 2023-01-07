import json
import string
import os
from datetime import datetime

import aiogram.utils.markdown as fmt
from aiogram import types

from loader import dp, bot
from settings.config import g_pidsluhano_id


@dp.message_handler(state="*")
async def all_text_messages(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open(os.path.abspath('scripts/cenzor_convertor/cenzor.json'))))) != set():
        if message.from_user.username:
            await message.reply(
                f"@{message.from_user.username} матюкатись не гарно")
        else:
            await message.reply(
                text=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> "
                     f"Матюкатись не гарно",
                parse_mode=types.ParseMode.HTML
            )
        await message.delete()

    elif message.text.lower() == 'путін':
        await message.reply(f'Х{fmt.hspoiler("##л# ла ла ла ла")}!\n(самі розумієте, матюки це погано:( ',
                            disable_notification=True)

    elif message.text.lower() == 'слава україні':
        await message.reply(f'Героям слава!', disable_notification=True)

    elif message.text.lower() == 'україна':
        await message.reply(f'Понад усе!', disable_notification=True)

    elif message.text.lower() == 'слава нації':
        await message.reply(f'Смерть ворогам!', disable_notification=True)

    if message.chat.id == g_pidsluhano_id:
        await bot.send_message(-1001636677869,
                               text=f"Група: <a href='t.me/{message.chat.username}'>"
                                    f"\"{message.chat.title}\"</a>\n"
                                    f"Користувач: <a href='tg://user?id={message.from_user.id}'>"
                                    f"{message.from_user.full_name}</a>"
                                    f" написав:\n[{datetime.now().strftime('%d.%m.%y о %H:%M')}]\n\n{message.text}",
                               disable_web_page_preview=True)
