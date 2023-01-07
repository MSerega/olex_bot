from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from loader import dp, bot


class FSMAdmin(StatesGroup):
    title = State()
    description = State()
    poster = State()
    link = State()


@dp.message_handler(commands='films')
async def cm_add_film(message: types.Message):
    await FSMAdmin.title.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('📤 Відміна')
    await message.answer("Введіть назва фільма", reply_markup=markup)


@dp.message_handler(Text(equals="📤 Відміна"), state=FSMAdmin.title)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Додавання фільму відмінено",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSMAdmin.title)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await FSMAdmin.next()
    await message.answer('Введіть опис фільма')


@dp.message_handler(state=FSMAdmin.description)
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer('Додайте постер фільма')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.poster)
async def set_poster(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['poster'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Введіть посилання на сайт, де можна переглянути фільм', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSMAdmin.link)
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

        keyboard = types.InlineKeyboardMarkup()
        online = types.InlineKeyboardButton('🖥 Дивитись онлайн', url=f"{data['link']}")
        watching = types.InlineKeyboardButton('❌ Статус: не переглянутий', callback_data="change_status_but:yes")
        keyboard.row(online).row(watching)

        await bot.send_photo(-1001269886962, data['poster'],
                             caption=f"<b>{data['title']}</b>\n\n{data['description']}",
                             reply_markup=keyboard)

    await state.finish()


@dp.callback_query_handler(text_startswith="change_status_but:")
async def edit_button_text(call: types.CallbackQuery):
    message_id = call.message.message_id
    chat_id = call.message.chat.id

    link = call.message.reply_markup.inline_keyboard[0][0].url
    print(link)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('🖥 Дивитись онлайн', url=f"{link}"))

    if call.data.split(":")[1] == 'yes':
        keyboard.row(types.InlineKeyboardButton('✅ Статус: Переглянутий', callback_data="change_status_but:no"))
    else:
        keyboard.row(types.InlineKeyboardButton('❌ Статус: не переглянутий', callback_data="change_status_but:yes"))

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
