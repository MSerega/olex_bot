from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from settings.config import ADMIN, c_pidsluhano_id, g_pidsluhano_id


class FSMAdmin(StatesGroup):
    chat_id = State()
    message_text = State()
    btns = State()
    btn_name = State()
    btn_link = State()


@dp.message_handler(commands='sender', chat_id=ADMIN)
async def cmd_sender(message: types.Message):
    await FSMAdmin.chat_id.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .row('📢 Канал', '👩‍👩‍👧‍👧 Група').row('📤 Відміна')
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
    if message.text == '📢 Канал':
        async with state.proxy() as data:
            data['chat_id'] = c_pidsluhano_id
    elif message.text == '👩‍👩‍👧‍👧 Група':
        async with state.proxy() as data:
            data['chat_id'] = g_pidsluhano_id
    elif message.forward_from:
        async with state.proxy() as data:
            data['chat_id'] = message.forward_from.id
    else:
        async with state.proxy() as data:
            data['chat_id'] = message.text
    await FSMAdmin.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('📤 Відміна')
    await message.answer('Введіть текст', reply_markup=markup)
    await bot.reply_to_message()


@dp.message_handler(state=FSMAdmin.message_text)
async def message_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_text'] = message.text
    await FSMAdmin.btns.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('Так', 'Ні').row('📤 Відміна')
    await message.answer('Ви будете довати з кнопкою чи без', reply_markup=markup)


@dp.message_handler(Text(equals=['Так', 'Ні']), state=FSMAdmin.btns)
async def btn_yes(message: types.Message, state: FSMContext):
    if message.text == 'Так':
        await FSMAdmin.btn_name.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('📤 Відміна')
        await message.answer('Введіть назву кнопки', reply_markup=markup)
    else:
        async with state.proxy() as data:
            await bot.send_message(data['chat_id'], data['message_text'], reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=FSMAdmin.btn_name)
async def btn_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_name'] = message.text
    await FSMAdmin.btn_link.set()
    await message.answer('Введіть посилання')


@dp.message_handler(state=FSMAdmin.btn_link)
async def btn_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_link'] = message.text

        keyboard = types.InlineKeyboardMarkup()
        link = types.InlineKeyboardButton(data['btn_name'], url=f"{data['btn_link']}")
        keyboard.row(link)

        await bot.send_message(data['chat_id'], data['message_text'], reply_markup=keyboard)

    await state.finish()

