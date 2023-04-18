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
    # Розваги
    menu_funs = State()
    # Розваги Бізнес центр порядок
    business_center_poradok = State()
    business_center_services = State()
    business_center_map = State()
    business_center_krasa = State()
    business_center_krasa_info = State()
    business_center_medicine = State()
    business_center_medicine_info = State()
    business_center_building = State()
    business_center_funs = State()
    business_center_funs_info = State()
    business_center_transport = State()


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
    if state_ in ['officeInsurance', 'internet_providers', 'menu_medicine', "menu_funs"]:
        await FSM_services.services.set()
        await message.answer("Оберіть послугу", reply_markup=kb.services_menu)
    if state_ in ['homeNet', 'svitNet']:
        await FSM_services.internet_providers.set()
        await message.answer("Оберіть провайдера", reply_markup=kb.internetProviders)

    if state_ in ['business_center_poradok']:
        await FSM_services.menu_funs.set()
        await message.answer("Оберіть послугу", reply_markup=kb.funs_menu)

    if state_ in ['business_center_services', 'business_center_map']:
        await FSM_services.business_center_poradok.set()
        await message.answer(f"🏢 Бізнес-центр \"Порядок\"\n\n"
                             "🗺 Адреса: смт Олександрівка,\n      вул. Пушкіна, 15\n\n"
                             "👩‍👦‍👦 Ми у Facebook: <a href=\"https://www.facebook.com/groups/565954754170059\">➕ Приєднатись</a>",
                             reply_markup=kb.cmd_business_center_info, disable_web_page_preview=True)

    if state_ in ['business_center_krasa', 'business_center_medicine',
                  'business_center_building', 'business_center_funs', 'business_center_transport']:
        await FSM_services.business_center_services.set()
        await message.answer("Оберіть послугу", reply_markup=kb.cmd_business_center_services)

    if state_ in ['business_center_krasa_info']:
        await FSM_services.business_center_krasa.set()
        await message.answer("Оберіть послугу", reply_markup=kb.cmd_business_center_krasa)

    if state_ in ['business_center_medicine_info']:
        await FSM_services.business_center_medicine.set()
        await message.answer("Оберіть послугу", reply_markup=kb.cmd_business_center_medicine)

    if state_ in ['business_center_funs_info']:
        await FSM_services.business_center_funs.set()
        await message.answer("Оберіть послугу", reply_markup=kb.cmd_business_center_funs)

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
