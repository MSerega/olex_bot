from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from loader import dp
from keyboards import default as kb
from settings import functions


class FSM_services(StatesGroup):
    services = State()
    # Послуга страхування
    officeInsurance = State()
    userCode = State()
    driver_passport = State()
    technical_passport01 = State()
    technical_passport02 = State()
    phone_ownerCar = State()
    # Послуга Інтернет
    internet_providers = State()
    homeNet = State()
    svitNet = State()
    # Медицина
    menu_medicine = State()
    reception = State()
    veterinarians = State()


@dp.message_handler(text="🗄 Послуги", chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_services(message: types.Message):
    await functions.userInDb(message)
    await FSM_services.services.set()
    await message.answer("Оберіть послугу",
                         reply_markup=kb.services_menu,
                         disable_notification=True)


@dp.message_handler(Text(equals="👈️ Назад"), state=FSM_services)
async def back_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_ = current_state.split(':')[1]
    if state_ in ['officeInsurance', 'internet_providers', 'menu_medicine']:
        await FSM_services.services.set()
        await message.answer("Оберіть послугу", reply_markup=kb.services_menu)
    if state_ in ['homeNet', 'svitNet']:
        await FSM_services.internet_providers.set()
        await message.answer("Оберіть провайдера", reply_markup=kb.internetProviders)
    if state_ in ['reception', 'veterinarians']:
        await FSM_services.menu_medicine.set()
        await message.answer("Оберіть послугу", reply_markup=kb.medicine_menu)
    elif state_ == 'services':
        if current_state is None:
            return
        await state.finish()
        await message.answer("Ви в головному меню. Оберіть пункт меню", reply_markup=kb.main_menu)


@dp.message_handler(Text(equals="📤 Скасувати"), state=FSM_services)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ви скасували послугу", reply_markup=kb.services_menu)
