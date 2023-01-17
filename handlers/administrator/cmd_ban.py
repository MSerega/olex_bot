import locale

from aiogram import types
from babel.dates import format_timedelta

from loader import dp
from settings.functions import parse_timedelta_from_message, parse_mute_comment


@dp.message_handler(commands=["ban"], is_admin=True)
async def cmd_ban(message: types.Message):
    await message.delete()
    duration = await parse_timedelta_from_message(message)
    comment = await parse_mute_comment(message)
    if not duration:
        return
    if comment is None:
        comment = ''
    try:
        await message.chat.kick(message.reply_to_message.from_user.id, until_date=duration)

    except Exception as e:
        await message.reply_to_message.answer(f'виникла помилка:\n{e}')
        return False

    await message.answer(
        "Учасник: {user}\nбув заблокований в чаті адміністратором.\nТермін: {duration}.\n{comment}".format(
            user=message.reply_to_message.from_user.get_mention(),
            admin=message.from_user.get_mention(),
            duration=format_timedelta(
                duration, granularity="seconds", format="short", locale=locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8'),
            ),
            comment=comment,
        ))
    return True
