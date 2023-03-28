from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from loader import dp
from keyboards import default as kb
from settings import functions


class FSM_poshta(StatesGroup):
    poshta = State()
    ukrposhta = State()
    ukr_info = State()
    novaposhta = State()
    nova_info = State()


@dp.message_handler(text="🚚 Пошта", chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_poshta(message: types.Message):
    await functions.userInDb(message)
    await FSM_poshta.poshta.set()
    await message.answer("Оберіть пункт меню",
                         reply_markup=kb.poshta,
                         disable_notification=True)


@dp.message_handler(Text(equals="👈️ Назад"), state=FSM_poshta)
async def back_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_ = current_state.split(':')[1]
    if state_ in ['ukrposhta', 'novaposhta']:
        await FSM_poshta.poshta.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.poshta)
    elif state_ == 'nova_info':
        await FSM_poshta.novaposhta.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.novaposhta)
    elif state_ == 'ukr_info':
        await FSM_poshta.ukrposhta.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.ukrposhta)
    elif state_ == 'poshta':
        if current_state is None:
            return
        await state.finish()
        await message.answer("Ви в головному меню. Оберіть пункт меню", reply_markup=kb.main_menu)


@dp.message_handler(Text(equals="🚚 Укрпошта"), state=FSM_poshta.poshta)
async def poshta_ukr(message: types.Message, state: FSMContext):
    await message.answer("Оберіть пункт меню", reply_markup=kb.ukrposhta)
    await FSM_poshta.ukrposhta.set()


@dp.message_handler(Text(equals="🚚 Нова Пошта"), state=FSM_poshta.poshta)
async def poshta_ukr(message: types.Message, state: FSMContext):
    await message.answer("Оберіть пункт меню", reply_markup=kb.novaposhta)
    await FSM_poshta.novaposhta.set()


@dp.message_handler(Text(equals="📦 Відділення №1"), state=FSM_poshta.novaposhta)
async def novaposhta_post1(message: types.Message, state: FSMContext):
    await message.answer(
        f"<code><b>Відділення №1:</b>\n"
        "Адреса: смт Олександрівка (рай.центр), вул. Незалежності України, 106\n"
        "Цифрова адреса: 95277 / 1\n\n</code>",
        reply_markup=kb.back_btn)
    await FSM_poshta.nova_info.set()


@dp.message_handler(Text(equals="📦 Відділення №2"), state=FSM_poshta.novaposhta)
async def novaposhta_post2(message: types.Message, state: FSMContext):
    await message.answer(
        f"<code><b>Відділення №2:</b>\n"
        "Адреса: смт Олександрівка (рай.центр), вул.Шевченка, 17а\n"
        "Цифрова адреса: 95277 / 2\n\n</code>",
        reply_markup=kb.back_btn)
    await FSM_poshta.nova_info.set()


@dp.message_handler(Text(equals="🗓 Графік роботи"), state=FSM_poshta.novaposhta)
async def novaposhta_graffic(message: types.Message, state: FSMContext):
    await message.answer(
        f"<b>Графік роботи відділень Нової пошти:</b>\n"
        "Пн: 09:00-19:00\n"
        "Вт: 09:00-19:00\n"
        "Ср: 09:00-19:00\n"
        "Чт: 09:00-19:00\n"
        "Пт: 09:00-19:00\n"
        "Сб: 09:00-18:00\n"
        "Нд: 10:00-18:00",
        reply_markup=kb.back_btn)
    await FSM_poshta.nova_info.set()


@dp.message_handler(Text(equals="📦 Відділення"), state=FSM_poshta.ukrposhta)
async def ukrposhta_address(message: types.Message, state: FSMContext):
    await message.answer(
        f"<code><b>Відділення Укрпошти</b>\n"
        "Адреса: вул. Незалежності України, 17, смт Олександрівка, Кропивницький район, Кіровоградська область\n"
        "Індекс: 27300</code>",
        reply_markup=kb.back_btn)
    await FSM_poshta.ukr_info.set()


@dp.message_handler(Text(equals="🗓 Графік роботи"), state=FSM_poshta.ukrposhta)
async def ukrposhta_graffic(message: types.Message, state: FSMContext):
    await message.answer(
        f"<b>Графік роботи відділення Укрпошти:</b>\n"
        "Пн: 08:00-18:00\n"
        "Вт: 08:00-18:00\n"
        "Ср: 08:00-18:00\n"
        "Чт: 08:00-18:00\n"
        "Пт: 08:00-18:00\n"
        "Сб: 09:00-15:00\n",
        reply_markup=kb.back_btn)
    await FSM_poshta.ukr_info.set()

