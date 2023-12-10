import asyncio
from aiogram import types


from settings.config import ADMIN


async def set_commands(dp):
    await set_default_commands(dp)
    await set_admin_commands(dp, ADMIN)
    await set_users_commands(dp)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("vote_mute", "🚫 Заблокувати користувача"),
        ]
    )


async def set_admin_commands(dp, admin_id):
    await dp.bot.set_my_commands(
            [
                types.BotCommand("menu", "📋 Меню"),
                types.BotCommand("statistics", "📊 Статистика"),
                types.BotCommand("sender", "📨 Відправити повідомлення"),
                types.BotCommand("reboot_olex_bot", "🔄 Reload olex_bot"),
                types.BotCommand("reboot_alarm_bot", "🔄 Reload alarm_bot")
            ],
            scope=types.bot_command_scope.BotCommandScopeChat(admin_id)
        )
    await asyncio.sleep(1)


async def set_users_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", "📋 Меню"),
            types.BotCommand("news", "📄 Запропонувати новину"),
            types.BotCommand("advertising", "💶 Замовити рекламу"),
            types.BotCommand("support", "👮‍ Технічна підтримка"),
        ],
        scope=types.bot_command_scope.BotCommandScopeAllPrivateChats()
    )
    await asyncio.sleep(1)

