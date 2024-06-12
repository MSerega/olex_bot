from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot


# Клас зі станами для FSM
class EditMessage(StatesGroup):
    waiting_for_message = State()  # Очікуємо переслане повідомлення
    waiting_for_new_text = State()  # Очікуємо новий текст для редагування


@dp.message_handler(commands=['edit'])
async def start_editing(message: types.Message):
    await message.answer("Перешліть повідомлення, яке ви хочете редагувати.")
    await EditMessage.waiting_for_message.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=EditMessage.waiting_for_message)
async def receive_message_to_edit(message: types.Message, state: FSMContext):
    if message.forward_from:
        async with state.proxy() as data:
            data['chat_id'] = message.forward_from.id
            data['message_id'] = message.message_id

        await message.reply("Тепер введіть новий текст повідомлення.")
        await EditMessage.waiting_for_new_text.set()
    else:
        await message.reply("Будь ласка, перешліть повідомлення з текстом для редагування.")



@dp.message_handler(content_types=types.ContentTypes.TEXT, state=EditMessage.waiting_for_new_text)
async def edit_message_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            chat_id = data['chat_id']
            message_id = data['message_id']
            new_text = message.text

            # Редагуємо повідомлення з новим текстом
            await bot.edit_message_text(new_text, chat_id, message_id, parse_mode=types.ParseMode.MARKDOWN)
            await message.reply("Повідомлення було успішно змінено!")

        except Exception as e:
            await message.reply(f"Помилка під час редагування повідомлення: {e}")

    # Перехід до початкового стану після успішного редагування або помилки
    await state.finish()
