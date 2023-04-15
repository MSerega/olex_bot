from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp
from keyboards import default as kb
from .states_services import FSM_services


@dp.message_handler(Text(equals="🚑 Медицина"), state=FSM_services.services)
async def cmd_menu_medicine(message: types.Message, state: FSMContext):
    await message.answer("Оберіть розділ медицини", reply_markup=kb.medicine_menu)
    await FSM_services.menu_medicine.set()


@dp.message_handler(Text(equals="🏥 Лікарня"), state=FSM_services.menu_medicine)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"🏫 Назва лікарні:\nКомунальне некомерційне підприємство \"Олександрівська лікарня\" Олександрівської "
                         f"селищної ради Кропивницького району Кіровоградської Області\n\n"
                         f"📬 Адреса:\nсмт Олександрівка,\nвул. Шевченка, 57\n\n"
                         f"📱 Телефон реєстратури лікарні:\n +38(052)-423-30-70", reply_markup=kb.back_btn)
    await FSM_services.reception.set()


@dp.message_handler(Text(equals="🐶 Ветеринари"), state=FSM_services.menu_medicine)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer("Ветеринар: Сергій Андрійович Кульбачевський\n"
                         "📱 +38(066)-282-90-55", reply_markup=kb.back_btn)
    await FSM_services.veterinarians.set()
