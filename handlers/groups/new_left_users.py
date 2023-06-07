import asyncio
from aiogram import types

from loader import bot, dp
from settings import functions
from settings.config import g_pidsluhano_id


@dp.message_handler(content_types=['new_chat_members', 'left_chat_member'])
async def enter_message_from_new_left_users(message: types.Message):
    if message.left_chat_member is not None:
        await bot.delete_message(message.chat.id, message.message_id)

    elif message.new_chat_members is not None:
        await bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == g_pidsluhano_id:
            greeting = await bot.send_message(message.chat.id,
                                              f"<a href='{message.new_chat_members[0].url}'>"
                                              f"{message.new_chat_members[0].first_name}</a> вітаємо в "
                                              f"групі \"Олександрівка\".\n\nПрочитайте "
                                              f"<a href='https://t.me/c/1247030550/8939'>правила "
                                              f"групи</a> та дотримуйтесь їх.", disable_notification=True,
                                              disable_web_page_preview=True)
            asyncio.create_task(functions.delete_message(greeting, 60))

        else:
            greeting2 = await bot.send_message(message.chat.id,
                                               f"{message.new_chat_members[0].first_name} вітаємо в групі.",
                                               disable_notification=True)
            asyncio.create_task(functions.delete_message(greeting2, 60))


