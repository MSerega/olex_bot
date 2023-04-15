from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from loader import dp
from keyboards import default as kb
from scripts.train import get_passenger_trains, get_suburnan_trains
from settings import functions


class FSM_transport(StatesGroup):
    transport = State()
    bus = State()
    taxi = State()
    trains = State()
    suburban_trains = State()
    passenger_trains = State()
    vokzal = State()


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
    if state_ in ['suburban_trains', 'passenger_trains', 'vokzal']:
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


@dp.message_handler(Text(equals="🚕 Таксі"), state=FSM_transport.transport)
async def cmd_taxi(message: types.Message, state: FSMContext):
    await message.answer(
        f"Перелік водіїв таксі, яких можна замовити по Олександрівці:\n\n"
        f"📱 +38(096)-139-14-72 - Іван\n\n"
        # f"📱 +38(098)-611-36-48 - Юра\n\n"
        f"📱 +38(098)-642-66-52 - Сергій\n\n"
        f"📱 +38(097)-179-92-46 - Віктор\n\n"
        f"📱 +38(097)-883-24-39 - Віталій\n\n"
        f"📱 +38(097)-774-45-64 - Андрій\n\n"
        f"📱 +38(098)-638-04-30 - Олександр\n\n"
        f"📱 +38(067)-377-34-51 - Микола\n\n"
        f"📱 +38(096)-990-97-20 - Сергій\n\n"
        f"📱 +38(096)-004-47-89 - Андрій\n\n"
        f"📱 +38(098)-780-93-57 - Віталій\n\n"
        f"📱 +38(098)-637-98-05 - Ігор\n\n"
        f"📱 +38(095)-808-75-33 - Люкс таксі\n\n"
        f"📱 +38(067)-520-37-41 - Люкс таксі\n\n"
        f"📱 +38(098)-801-54-80 - Нове таксі\n\n" + kb.links, reply_markup=kb.back_btn)
    await FSM_transport.taxi.set()


@dp.message_handler(Text(equals="🚌 Автобуси"), state=FSM_transport.transport)
async def cmd_bus(message: types.Message, state: FSMContext):
    await message.answer(
        f"Розклад руху автобусів через Олександрівку:\n\n"
        f"Олександрівка - Кропивницький:\n"
        f"⏱ 06:00, ⏱ 07:00, ⏱ 09:50, ⏱ 11:20,\n"
        f"⏱ 12:00, ⏱ 13:25, ⏱ 16:30\n\n"
        f"Кропивницький - Олександрівка:\n"
        f"⏱ 07:30, ⏱ 08:50, ⏱ 10:00, ⏱ 12:20,\n"
        f"⏱ 12:30, ⏱ 14:20, ⏱ 15:20, ⏱ 16:00" + kb.links, reply_markup=kb.back_btn)
    await FSM_transport.bus.set()


@dp.message_handler(Text(equals="🚞 Приміські поїзди"), state=FSM_transport.trains)
async def suburban_trains(message: types.Message, state: FSMContext):
    trains_list = get_suburnan_trains()
    trains_s = ''
    for train in trains_list:
        trains_s += f"🚊 Поїзд №: {train['number']}\n" \
                    f"📅 Період: {train['days']}\n" \
                    f"📋 Маршрут: {train['way']}\n" \
                    f"🕰 Час прибуття: {train['time_start']}\n" \
                    f"⏱ Зупинка: {train['time_stop']}\n" \
                    f"🕰 Час відправлення: {train['time_end']}\n\n"
    await message.answer(f"Розклад руху приміських поїздів через станцію Фундукліївка:\n\n" + trains_s + kb.links,
                         reply_markup=kb.back_btn)
    await FSM_transport.suburban_trains.set()


@dp.message_handler(Text(equals="🚞 Пасажирські поїзди"), state=FSM_transport.trains)
async def suburban_trains(message: types.Message, state: FSMContext):
    trains_list = get_passenger_trains()
    trains_p = ''
    for train in trains_list:
        trains_p += f"🚊 Поїзд №: {train['number']}\n" \
                    f"📅 Період: {train['days']}\n" \
                    f"📋 Маршрут: {train['way']}\n" \
                    f"🕰 Час прибуття: {train['time_start']}\n" \
                    f"⏱ Зупинка: {train['time_stop']}\n" \
                    f"🕰 Час відправлення: {train['time_end']}\n\n"
    await message.answer(f"Розклад руху пасажирських поїздів через станцію Фундукліївка:\n\n" + trains_p + kb.links,
                         reply_markup=kb.back_btn)
    await FSM_transport.passenger_trains.set()


@dp.message_handler(Text(equals="🏫 Заліжничний вокзал"), state=FSM_transport.trains)
async def suburban_trains(message: types.Message, state: FSMContext):
    await message.answer(f"Номер телефону станції Фундукліївка: \n\n📱 +38(052)423-27-10" + kb.links, reply_markup=kb.back_btn)
    await FSM_transport.vokzal.set()
