from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot


class IsLink(BoundFilter):
    async def check(self, msg: types.Message):
        for i in msg.entities:
            if i.type == "url":
                return True
        for i in msg.caption_entities:
            if i.type == "url":
                return True
            elif i.type == "text_link":
                return True


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, msg: types.Message):
        result = (await bot.get_chat_member(msg.chat.id, msg.from_user.id)).is_chat_admin()
        if msg.from_user.username == 'GroupAnonymousBot':
            result = True
        if msg.from_user.id == 777000:
            result = True
        if self.is_admin == result:
            return True

