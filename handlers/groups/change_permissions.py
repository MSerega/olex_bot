from aiogram.types import ChatPermissions, InputFile

from settings.config import g_pidsluhano_id, c_pidsluhano_id
from loader import bot


async def message_permissions_block():
    await bot.set_chat_permissions(g_pidsluhano_id,
                                   permissions=ChatPermissions(can_send_messages=False,
                                                               can_invite_users=True))
    await bot.send_photo(c_pidsluhano_id, InputFile("images/comendant.jpg"),
                         caption="На території Олександрівської територіальної громади запроваджено комендантську "
                                 "годину.\n\n<b>З 23:00 до 5:00</b> <b>забороняється</b> перебування у визначений "
                                 "період доби на вулицях та в інших громадських місцях осіб без виданих перепусток,"
                                 " а також рух транспортних засобів.\n\n"
                                 "З 23:00 до 7:00 В групі введено режим тиші, спілкування обмежено.")


async def message_permissions_access():
    await bot.set_chat_permissions(g_pidsluhano_id,
                                   permissions=ChatPermissions(can_send_messages=True,
                                                               can_invite_users=True,
                                                               can_send_media_messages=True,
                                                               can_send_other_messages=True
                                                               ))
