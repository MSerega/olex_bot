from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from keyboards.inline_support.support import support_keyboard, support_callback
from loader import dp, bot
from settings.functions import delete_message
from settings.config import SUPPORT_ADMINS


@dp.message_handler(commands=['support'], chat_type=types.ChatType.PRIVATE, state="*")
async def ask_support(message: types.Message):
    text = "Хочете написати повідомлення в технічну підтримку?\nНатисніть на кнопку нижче!"
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="one"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get("user_id"))
    your_message = await call.message.answer("Напишіть ваше повідомлення")
    await state.set_state("wait_for_support_message")
    await state.update_data(second_id=user_id)
    await delete_message(your_message, 5)


@dp.message_handler(state="wait_for_support_message", content_types=types.ContentTypes.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)

    for ADMIN in SUPPORT_ADMINS:
        if second_id == ADMIN:
            user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            text = f"Користувач: {user_link}\n{message.text}"
            await bot.send_message(second_id, text, reply_markup=keyboard)
        else:
            await message.copy_to(second_id, reply_markup=keyboard)
    await state.reset_state()
