from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp
from keyboards import default as kb
from .states_services import FSM_services


@dp.message_handler(Text(equals="🎮 Розваги"), state=FSM_services.services)
async def cmd_menu_medicine(message: types.Message, state: FSMContext):
    await message.answer("Оберіть пункт меню", reply_markup=kb.funs_menu)
    await FSM_services.menu_funs.set()


@dp.message_handler(Text(equals="🏢 Бізнес-центр \"Порядок\""), state=FSM_services.menu_funs)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Бізнес-центр \"Порядок\"\n"
                         "Адреса: смт Олександрівка, вул. Пушкіна, 15\n\n"
                         "<b>Надаємо перелік послуг:</b>\n"
                         "- Манікюр\n"
                         "- Парикмахер\n"
                         "- Візажист\n"
                         "- Косметолог\n"
                         "- Масажист\n"
                         "- Стоматологія\n"
                         "- Перевезення\n"
                         "- Виробництво мангалів, автоклавів, коптилень, спортивних товарів, тощо.\n\n"
                         "Телефони бізнес-центру:\n"
                         "📱 +38(097)953-67-09\n"
                         "📱 +38(068)349-64-41", reply_markup=kb.cmd_business_center_info)
    await FSM_services.business_center_poradok.set()


@dp.message_handler(Text(equals="🏢 Бізнес-центр \"Порядок\""), state=FSM_services.business_center_poradok)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть пункт меню", reply_markup=kb.cmd_business_center_info)
    await FSM_services.business_center_poradok.set()


@dp.message_handler(Text(equals="🧾 Послуги"), state=FSM_services.business_center_poradok)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_services)
    await FSM_services.business_center_services.set()


@dp.message_handler(Text(equals="🙍‍♀ Краса"), state=FSM_services.business_center_services)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_krasa)
    await FSM_services.business_center_krasa.set()


@dp.message_handler(Text(equals="❤ Здоров\'я"), state=FSM_services.business_center_services)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_medicine)
    await FSM_services.business_center_medicine.set()


@dp.message_handler(Text(equals="🕹 Розваги"), state=FSM_services.business_center_services)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_funs)
    await FSM_services.business_center_funs.set()


@dp.message_handler(Text(equals="🛠 Виробництво"), state=FSM_services.business_center_services)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.back_btn)
    await FSM_services.business_center_building.set()
