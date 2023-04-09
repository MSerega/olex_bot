from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from keyboards import default as kb
from settings.config import ADMIN


class FSMAdmin(StatesGroup):
    title_news = State()
    text_news = State()


@dp.message_handler(commands='news', chat_type=types.ChatType.PRIVATE, state="*")
async def command_news(message: types.Message):
    await FSMAdmin.title_news.set()
    await message.answer("Вкажіть заголовок вашої новини", reply_markup=kb.cancel_fsm)


@dp.message_handler(Text(equals="📤 Скасувати"), state=FSMAdmin)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ви скасували додавання новини.",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSMAdmin.title_news)
async def set_title_news(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.chat.has_private_forwards:
            data['user_id'] = "Невідомий користувач"
        else:
            data['user_id'] = message.from_user.id
            data['title_news'] = message.text
    await FSMAdmin.next()
    await message.answer('Опишіть новину, якщо є фото також можете прикріпити, опис новини потрібно вказати під фото',
                         reply_markup=kb.cancel_fsm)


@dp.message_handler(content_types=['photo', 'text'], state=FSMAdmin.text_news)
async def set_text_news(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        kb_connect = types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton("✉ Зв'язатись з автором новини", url=f"tg://user?id={data['user_id']}"))
        if not message.text:
            data['photo_id'] = message.photo[0].file_id
            data['caption'] = message.caption
            await dp.bot.send_photo(ADMIN, data['photo_id'], caption=f"Є новина в групу "
                                                                     f"від користувача <code>{data['user_id']}</code>:\n"
                                                                     f"Заголовок: {data['title_news']}\n"
                                                                     f"Опис: {data['caption']}\n", reply_markup=kb_connect)
        else:
            data['text_news'] = message.text
            await dp.bot.send_message(ADMIN, f"Є новина в групу від користувача <code>{data['user_id']}</code>:\n"
                                             f"Заголовок: {data['title_news']}\n"
                                             f"Опис: {data['text_news']}\n", reply_markup=kb_connect)
    await state.finish()
    await message.answer("Дякуємо за новину. Після перевірки модератором, новина буде опублікована в групі.",
                         reply_markup=types.ReplyKeyboardRemove())
