import asyncio
import datetime

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.exceptions import Throttled
from loader import dp, bot
from settings import functions
from settings.config import SUPPORT_ADMINS


@dp.message_handler(commands=["vote_mute"],
                    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    state="*")
async def cmd_vote_mute(message: types.Message):
    try:
        await dp.throttle('vote_mute', rate=2)
    except Throttled:
        await message.reply('Забагато запитів, спробуйте через 2 секунд.')
    else:
        if not message.reply_to_message:
            msg = await message.answer_photo(InputFile('images/votemute.jpg'),
                                             "Ця команда повинна бути відповіддю на повідомлення!"
                                             "\n\nВиберіть повідомлення користувача, натисніть в меню <b>Відповісти</b> "
                                             "і після цього викличіть команду для блоку.")
            asyncio.create_task(functions.delete_message(msg, 60))
            await message.delete()
        else:
            banned_user = message.reply_to_message.from_user
            voter_user = message.from_user
            status_user = await bot.get_chat_member(message.chat.id, banned_user.id)
            duration = datetime.timedelta(hours=1)
            if banned_user.id in SUPPORT_ADMINS:
                msg = await message.answer(
                    "Адміністраторів групи не можна заблокувати, хто ж буде слідкувати за порядком?")
                asyncio.create_task(functions.delete_message(msg, 60))
            elif status_user.status != "restricted":
                await message.delete()
                await message.answer(f"Користувач <a href=\"{voter_user.url}\">{voter_user.full_name}</a> "
                                     f"хоче заблокувати користувача "
                                     f"<a href=\"{banned_user.url}\">{banned_user.full_name}</a>."
                                     f"\nГолосування триватиме 5 хвилин. "
                                     f"Якщо буде набрано 10 голосів, користувача буде заблоковано.")
                msg = await bot.send_poll(chat_id=message.chat.id, is_anonymous=False,
                                          question=f"Бажаєте заблокувати користувача {banned_user.full_name}?",
                                          options=["Заблокувати", "Пробачити"])
                await asyncio.sleep(300)
                poll = await bot.stop_poll(chat_id=message.chat.id, message_id=msg.message_id)

                if poll.options[0].voter_count >= 10:
                    await message.chat.restrict(banned_user.id, can_send_messages=False, until_date=duration)
                    await message.answer(
                        f"Користувача <a href=\"{banned_user.url}\">{banned_user.full_name}</a> заблоковано "
                        f"на 1 годину.")
                else:
                    await message.answer(f"Шановний <a href=\"{banned_user.url}\">{banned_user.full_name}</a>, "
                                         "після результатів голосування було вирішино не блокувати вас, але "
                                         "задумайтесь над тим, чому вас виставили на голосування")
            else:
                msg = await message.answer(f"Користувача <a href=\"{banned_user.url}\">{banned_user.full_name}</a> "
                                           "не можна заблокувати, тому що він вже заблокований.")
                asyncio.create_task(functions.delete_message(msg, 60))

