import asyncio
from contextlib import suppress
from shlex import join

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

import datetime
import re
import typing

from db import db_connect


async def userInDb(message: types.Message):
    if not db_connect.user_exists(message.from_user.id):
        tg_user = [message.from_user.id,
                   message.from_user.username,
                   message.from_user.first_name,
                   message.from_user.last_name,
                   message.from_user.full_name]
        db_connect.add_users(tg_user)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


PATTERN = re.compile(r"(?P<value>\d+)(?P<modifier>[wdhms])")
LINE_PATTERN = re.compile(r"^(\d+[wdhms]){1,}$")

MODIFIERS = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str) -> datetime.timedelta:
    match = LINE_PATTERN.match(value)
    if not match:
        raise TimedeltaParseError("Час вказаний не вірно")

    try:
        result = datetime.timedelta()
        for match in PATTERN.finditer(value):
            value, modifier = match.groups()

            result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        raise TimedeltaParseError("Час надто великий")

    return result


async def parse_timedelta_from_message(message: types.Message, ) -> typing.Optional[datetime.timedelta]:
    _, *args = message.text.split()
    if args:
        try:
            duration = parse_timedelta(args[0])
        except TimedeltaParseError:
            await message.reply("Помилка обробки часу")
            return
        if duration <= datetime.timedelta(seconds=30):
            return datetime.timedelta(seconds=30)
        return duration
    else:
        return datetime.timedelta(minutes=15)


async def parse_mute_comment(message: types.Message):
    if len(message.text.split()) > 2:
        comment = message.text.split()[2:]
        return f"Причина: " + " ".join(map(str, comment))
    else:
        return None
