import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot
import subprocess

from settings.config import ADMIN

BOTS = {
    '0': 'Olex_bot',
    '1': 'Alarm_bot'
}

# Команда /control_bot
@dp.message_handler(commands=['control_bot'], chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def control_bot(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text=BOTS['0'], callback_data="select_bot_0"),
        InlineKeyboardButton(text=BOTS['1'], callback_data="select_bot_1")
    )
    await message.answer("Оберіть бота:", reply_markup=keyboard)


# Обробник вибору бота
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('select_bot_'), chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def process_bot_selection(callback_query: types.CallbackQuery):
    bot_id = callback_query.data.split('_')[-1]
    bot_name = BOTS[bot_id]
    await bot.answer_callback_query(callback_query.id)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text="Перезапустити бота", callback_data=f"restart_bot_{bot_id}"),
        InlineKeyboardButton(text="Зупинити бота", callback_data=f"stop_bot_{bot_id}")
    )
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=f"Оберіть дії з ботом {bot_name}:",
                                reply_markup=keyboard)


# Обробник дій з ботом
@dp.callback_query_handler(lambda c: c.data and (c.data.startswith('stop_bot_') or c.data.startswith('restart_bot_')), chat_type=types.ChatType.PRIVATE, chat_id=ADMIN, state="*")
async def process_bot_action(callback_query: types.CallbackQuery):
    action, bot_id = callback_query.data.split('_')[0], callback_query.data.split('_')[-1]
    bot_name = BOTS[bot_id]
    await bot.answer_callback_query(callback_query.id)

    if action == 'stop':
        try:
            subprocess.call(["pm2", "stop", f"{bot_id}"])
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"Бот {bot_name} зупинено.")
        except subprocess.CalledProcessError:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"Помилка зупинки бота {bot_name}.")
    elif action == 'restart':
        try:
            subprocess.call(["pm2", "restart", f"{bot_id}"])
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"Бот {bot_name} перезавантажено.")
        except subprocess.CalledProcessError:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"Помилка перезавантаження бота {bot_name}.")
