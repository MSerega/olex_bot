from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from db import db_connect as db
from loader import dp
from settings.config import ADMIN


class FSMAdmin(StatesGroup):
    station = State()
    fuel = State()
    accept = State()


stations = {
    '⛽ Shell': types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False,
        keyboard=[['⛽ А-92', '⛽ А-95'], ['⛽ ДП', '⛽ Газ'], ['💾 Зберегти'], ['👈️ Назад']]),
    '⛽ MAC': types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False,
        keyboard=[['⛽ А-92', '⛽ А-95', '⛽ ДП'], ['💾 Зберегти'], ['👈️ Назад']]),
    '⛽ Belarus': types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False,
        keyboard=[['⛽ Газ'], ['💾 Зберегти'], ['👈️ Назад']])
}


@dp.message_handler(commands="fuels", chat_id=ADMIN)
@dp.message_handler(Text(equals="⛽ Наявність пального", ignore_case=True), state="*")
async def fuels_start(message: types.Message):
    await FSMAdmin.station.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .add('⛽ Shell', '⛽ MAC', '⛽ Belarus').add('📤 Вийти з адмін панелі')
    await message.answer("Оберіть заправку", reply_markup=markup, disable_notification=True)


@dp.message_handler(Text(equals="📤 Вийти з адмін панелі"), state=FSMAdmin.station)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ви вийшли з адмін панелі. Тепер вам доступні команди бота",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="👈️ Назад"), state=['station', 'fuel', 'accept'])
async def back_state(message: types.Message, state: FSMContext):
    global stations

    current_state = await state.get_state()
    if current_state.split(':')[1] == 'fuel':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
            .add('⛽ Shell', '⛽ MAC', '⛽ Belarus').add('📤 Вийти з адмін панелі')
        await message.answer("Оберіть заправку", reply_markup=markup, disable_notification=True)
        await state.reset_data()
        await FSMAdmin.previous()
    if current_state.split(':')[1] == 'accept':
        stations_name = {
            'Shell': '⛽ Shell',
            'Mac': '⛽ MAC',
            'Belarus': '⛽ Belarus',
        }
        markup = stations[stations_name[(await state.get_data())['station']]]
        await message.answer("Оберіть пальне", reply_markup=markup, disable_notification=True)
        await FSMAdmin.previous()


@dp.message_handler(state=FSMAdmin.station)
async def set_station(message: types.Message, state: FSMContext):
    global stations
    stations_name = {
        '⛽ Shell': 'Shell',
        '⛽ MAC': 'Mac',
        '⛽ Belarus': 'Belarus',
    }

    async with state.proxy() as data:
        data['station'] = stations_name[message.text]

    await message.answer("Вкажіть наявність пального",
                         reply_markup=stations[message.text],
                         disable_notification=True)
    await FSMAdmin.next()


@dp.message_handler(Text(equals="💾 Зберегти", ignore_case=True), state="*")
@dp.message_handler(state="*", commands="/Зберегти")
async def save_fuel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    async with state.proxy() as data:
        print(data)
    await db.update_db(state)
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .add('⛽ Shell', '⛽ MAC', '⛽ Belarus').add('📤 Вийти з адмін панелі')
    await message.answer("Дані успішно збережені", reply_markup=markup, disable_notification=True)
    await FSMAdmin.station.set()


@dp.message_handler(Text(equals=["⛽ А-95", "⛽ А-92", "⛽ ДП", "⛽ Газ"]), state=FSMAdmin.fuel)
async def set_fuel(message: types.Message, state: FSMContext):
    dict_fuel = {
        "⛽ А-95": "fuel_95",
        "⛽ А-92": "fuel_92",
        "⛽ ДП": "fuel_diezel",
        "⛽ Газ": "fuel_gaz"
    }
    async with state.proxy() as data:
        data.setdefault("choise_fuel", {})
        data['choise_fuel'][dict_fuel[message.text]] = None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('✅ Так', '❌ Ні').add(
        '👈️ Назад')

    await message.answer("Бензин в наявності", reply_markup=markup, disable_notification=True)
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.accept)
async def btn_yes_no(message: types.Message, state: FSMContext):
    global stations

    async with state.proxy() as data:
        for key, value in data["choise_fuel"].items():
            if value is None:
                data["choise_fuel"][key] = 1 if "✅ Так" == message.text else 0
                break

    stations_name = {
        'Shell': '⛽ Shell',
        'Mac': '⛽ MAC',
        'Belarus': '⛽ Belarus',
    }
    await message.answer("Виберіть пальне", reply_markup=stations[stations_name[(await state.get_data())['station']]])
    await FSMAdmin.fuel.set()
