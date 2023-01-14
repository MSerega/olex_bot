from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from loader import dp
from keyboards import default as kb
from scripts.train import get_trains
from settings import functions


class FSM_transport(StatesGroup):
    transport = State()
    bus = State()
    taxi = State()
    trains = State()
    suburban_trains = State()
    passenger_trains = State()


@dp.message_handler(text="🚌 Транспорт", chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_poshta(message: types.Message):
    await functions.userInDb(message)
    await FSM_transport.transport.set()
    await message.answer("Оберіть пункт меню",
                         reply_markup=kb.transport_menu,
                         disable_notification=True)


@dp.message_handler(Text(equals="👈️ Назад"), state=FSM_transport)
async def back_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_ = current_state.split(':')[1]
    if state_ in ['bus', 'taxi', 'trains']:
        await FSM_transport.transport.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.transport_menu)
    if state_ in ['suburban_trains', 'passenger_trains']:
        await FSM_transport.trains.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.trains_menu)
    elif state_ == 'transport':
        if current_state is None:
            return
        await state.finish()
        await message.answer("Ви в головному меню. Оберіть пункт меню", reply_markup=kb.main_menu)


@dp.message_handler(Text(equals="🚋 Поїзди"), state=FSM_transport.transport)
async def trains(message: types.Message, state: FSMContext):
    await message.answer("Оберіть пункт меню", reply_markup=kb.trains_menu)
    await FSM_transport.trains.set()


@dp.message_handler(Text(equals="🚌 Автобуси"), state=FSM_transport.transport)
async def poshta_ukr(message: types.Message, state: FSMContext):
    await message.answer(
        f"Розклад руху автобусів через Олександрівку:\n\n"
        f"Олександрівка - Кропивницький:\n"
        f"⏱ 06:00, ⏱ 07:00, ⏱ 09:50, ⏱ 11:20,\n"
        f"⏱ 12:00, ⏱ 13:25, ⏱ 16:30\n\n"
        f"Кропивницький - Олександрівка:\n"
        f"⏱ 07:30, ⏱ 08:50, ⏱ 10:00, ⏱ 12:20,\n"
        f"⏱ 12:30, ⏱ 14:20, ⏱ 15:20, ⏱ 16:00\n\n"

        f"з 20 грудня 2022 року по 20 січня 2023 року\n\n"
        f"Олександрівка - Кропивницький:\n"
        f"⏱ 7.45\n\n" 
        f"Кропивницький - Олександрівка:\n"
        f"⏱ 17.30", reply_markup=kb.back_btn)
    await FSM_transport.bus.set()


@dp.message_handler(Text(equals="🚌 Автобуси"), state=FSM_transport.transport)
async def poshta_ukr(message: types.Message, state: FSMContext):
    await message.answer(
        f"Розклад руху автобусів через Олександрівку:\n\n"
        f"Олександрівка - Кропивницький:\n"
        f"⏱ 06:00, ⏱ 07:00, ⏱ 09:50, ⏱ 11:20,\n"
        f"⏱ 12:00, ⏱ 13:25, ⏱ 16:30\n\n"
        f"Кропивницький - Олександрівка:\n"
        f"⏱ 07:30, ⏱ 08:50, ⏱ 10:00, ⏱ 12:20,\n"
        f"⏱ 12:30, ⏱ 14:20, ⏱ 15:20, ⏱ 16:00\n\n"

        f"з 20 грудня 2022 року по 20 січня 2023 року\n\n"
        f"Олександрівка - Кропивницький:\n"
        f"⏱ 7.45\n\n" 
        f"Кропивницький - Олександрівка:\n"
        f"⏱ 17.30", reply_markup=kb.back_btn)
    await FSM_transport.bus.set()


@dp.message_handler(Text(equals="🚞 Приміські поїзди"), state=FSM_transport.trains)
async def suburban_trains(message: types.Message, state: FSMContext):
    trains_list = get_trains()
    trains = ''
    for train in trains_list:
        trains += f"🚊 Поїзд №: {train['number']}\n" \
                 f"📅 Період: {train['days']}\n" \
                 f"📋 Маршрут: {train['way']}\n" \
                 f"🕰 Час прибуття: {train['time_start']}\n" \
                 f"🕰 Час відправлення: {train['time_end']}\n\n"
    await message.answer(f"Розклад руху приміських поїздів через станцію Фундукліївка:\n\n" + trains,
                         reply_markup=kb.back_btn)
    await FSM_transport.suburban_trains.set()

