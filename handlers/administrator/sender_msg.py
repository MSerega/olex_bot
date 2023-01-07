from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from keyboards.default import links
from settings.config import ADMIN


class FSMAdmin(StatesGroup):
    chat_id = State()
    message_text = State()
    btn_name = State()
    btn_link = State()


@dp.message_handler(commands='sender', chat_id=ADMIN)
async def cmd_sender(message: types.Message):
    await FSMAdmin.chat_id.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .row('-1001466681334', '-1001247030550').row('📤 Відміна')
    await message.answer("Введіть id чата", reply_markup=markup)


@dp.message_handler(Text(equals="📤 Відміна"), state=FSMAdmin)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Відправку повідомлення відмінено",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSMAdmin.chat_id)
async def set_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await FSMAdmin.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('📤 Відміна')
    await message.answer('Введіть текст', reply_markup=markup)


@dp.message_handler(state=FSMAdmin.message_text)
async def message_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_text'] = message.text
    await FSMAdmin.next()
    await message.answer('Назва кнопки')


@dp.message_handler(state=FSMAdmin.btn_name)
async def btn_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_name'] = message.text
    await FSMAdmin.next()
    await message.answer('Введіть посилання')


@dp.message_handler(state=FSMAdmin.btn_link)
async def btn_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_link'] = message.text

        keyboard = types.InlineKeyboardMarkup()
        link = types.InlineKeyboardButton(data['btn_name'], url=f"{data['btn_link']}")
        keyboard.row(link)

        await bot.send_message(data['chat_id'], data['message_text'] + links, reply_markup=keyboard)

    await state.finish()


# @dp.callback_query_handler(text_startswith="change_status_but:")
# async def edit_button_text(call: types.CallbackQuery):
#     message_id = call.message.message_id
#     chat_id = call.message.chat.id
#
#     link = call.message.reply_markup.inline_keyboard[0][0].url
#     print(link)
#
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.row(types.InlineKeyboardButton('🖥 Дивитись онлайн', url=f"{link}"))
#
#     if call.data.split(":")[1] == 'yes':
#         keyboard.row(types.InlineKeyboardButton('✅ Статус: Переглянутий', callback_data="change_status_but:no"))
#     else:
#         keyboard.row(types.InlineKeyboardButton('❌ Статус: не переглянутий', callback_data="change_status_but:yes"))
#
#     await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
