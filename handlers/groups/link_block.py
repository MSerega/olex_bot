from filters.filters import IsLink
from aiogram import types
from settings.config import g_pidsluhano_id
from settings.functions import delete_message
from loader import dp


@dp.edited_message_handler(IsLink(), is_admin=False, chat_id=g_pidsluhano_id, content_types=types.ContentTypes.ANY)
@dp.message_handler(IsLink(), is_admin=False, chat_id=g_pidsluhano_id, content_types=types.ContentTypes.ANY)
async def block_links(message: types.Message):
    if message.from_user.username:
        linkmessage = await message.reply(
            f"@{message.from_user.username} Посилання в групі може писати лише адміністрація групи.")
        await message.delete()
        await delete_message(linkmessage, 10)
    else:
        linkmessage = await message.reply(
            text=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> "
                 f"Посилання в групі може писати лише адміністрація групи.",
            parse_mode=types.ParseMode.HTML
        )

        await message.delete()
        await delete_message(linkmessage, 10)
