import asyncio
import datetime

from aiogram import types
from loader import dp, bot
from settings.config import SUPPORT_ADMINS


@dp.message_handler(commands=["vote_mute"],
                    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    state="*")
async def cmd_mute(message: types.Message):
    banned_user = message.reply_to_message.from_user
    voter_user = message.from_user
    status_user = await bot.get_chat_member(message.chat.id, banned_user.id)
    duration = datetime.timedelta(hours=1)
    if not message.reply_to_message:
        await message.reply('Ця команда повинна бути відповіддю на повідомлення!')
    else:
        if banned_user.id in SUPPORT_ADMINS:
            await message.answer("Адміністраторів групи не можна заблокувати, хто ж буде слідкувати за порядком?")
        elif status_user.status != "restricted":
            await message.delete()
            await message.answer(f"Користувач <a href=\"{voter_user.url}\">{voter_user.full_name}</a>"
                                 f" хоче заблокувати користувача <a href=\"{banned_user.url}\">{banned_user.full_name}</a>."
                                 f"\nГолосування триватиме 5 хвилин. Якщо буде набрано 10 голосів, користувача буде заблоковано.")
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
            await message.answer(f"Користувача <a href=\"{banned_user.url}\">{banned_user.full_name}</a> "
                                 "не можна заблокувати, тому що він вже заблокований.")
