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
async def cmd_bissness_center_info(message: types.Message, state: FSMContext):
    await message.answer(f"🏢 Бізнес-центр \"Порядок\"\n"
                         "🗺 Адреса: смт Олександрівка, вул. Пушкіна, 15", reply_markup=kb.cmd_business_center_info)
    await FSM_services.business_center_poradok.set()


@dp.message_handler(Text(equals="🏢 Бізнес-центр \"Порядок\""), state=FSM_services.business_center_poradok)
async def cmd_bissness_center_poradok(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть пункт меню", reply_markup=kb.cmd_business_center_info)
    await FSM_services.business_center_poradok.set()


@dp.message_handler(Text(equals="🧾 Послуги"), state=FSM_services.business_center_poradok)
async def cmd_bissness_center_services(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_services)
    await FSM_services.business_center_services.set()


@dp.message_handler(Text(equals="🙍‍♀ Краса"), state=FSM_services.business_center_services)
async def cmd_bissness_center_krasa(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_krasa)
    await FSM_services.business_center_krasa.set()


@dp.message_handler(Text(equals="➡ Манікюр"), state=FSM_services.business_center_krasa)
async def cmd_bissness_center_krasa(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_krasa_info.set()


@dp.message_handler(Text(equals="➡ Парикмахер"), state=FSM_services.business_center_krasa)
async def cmd_bissness_center_krasa(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_krasa_info.set()


@dp.message_handler(Text(equals="➡ Візажист"), state=FSM_services.business_center_krasa)
async def cmd_bissness_center_krasa(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_krasa_info.set()


@dp.message_handler(Text(equals="❤ Здоров\'я"), state=FSM_services.business_center_services)
async def cmd_bissness_center_health(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_medicine)
    await FSM_services.business_center_medicine.set()


@dp.message_handler(Text(equals="➡ Масажист"), state=FSM_services.business_center_medicine)
async def cmd_bissness_center_masagist(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_medicine_info.set()


@dp.message_handler(Text(equals="➡ Стоматолог"), state=FSM_services.business_center_medicine)
async def cmd_bissness_center_stomatolog(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_medicine_info.set()


@dp.message_handler(Text(equals="➡ Косметолог"), state=FSM_services.business_center_medicine)
async def cmd_bissness_center_kosmetolog(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_medicine_info.set()


@dp.message_handler(Text(equals="🕹 Розваги"), state=FSM_services.business_center_services)
async def cmd_bissness_center_funs(message: types.Message, state: FSMContext):
    await message.answer(f"Оберіть послуги", reply_markup=kb.cmd_business_center_funs)
    await FSM_services.business_center_funs.set()


@dp.message_handler(Text(equals="🎱 Більярд"), state=FSM_services.business_center_funs)
async def cmd_bissness_center_bilyard(message: types.Message, state: FSMContext):
    await message.answer(f"🎱 Більярд\n"
                          f"🏙 Знаходиться: 2 поверх, кб. №11.\n\n"
                         f"🕰 Графік роботи:\n"
                         f"Щоденно: 🕖 08:00 - 🕚 23:00\n\n"
                         f"📱 Телефон: +38(097)953-67-09", reply_markup=kb.back_btn)
    await FSM_services.business_center_funs_info.set()


@dp.message_handler(Text(equals="👫 Розважальний центр"), state=FSM_services.business_center_funs)
async def cmd_bissness_center_funs_center(message: types.Message, state: FSMContext):
    await message.answer(f"👫 Розважальний центр «7Я».\n"
                         f"🏙 Знаходиться: 2 поверх, кб. №12.\n\n"
                         f"🕰 Графік роботи:\n"
                         f"Вт: 🕐 13:00 - 🕖 19:00\n"
                         f"Сб: 🕐 13:00 - 🕖 19:00\n\n"
                         f"📱 Телефон: +38(068)349-64-41", reply_markup=kb.back_btn)
    await FSM_services.business_center_funs_info.set()


@dp.message_handler(Text(equals="🛠 Виробництво"), state=FSM_services.business_center_services)
async def cmd_bissness_center_building(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_building.set()


@dp.message_handler(Text(equals="🚛 Перевезення"), state=FSM_services.business_center_services)
async def cmd_bissness_center_transport(message: types.Message, state: FSMContext):
    await message.answer(f"Додати послугу можна зв'язавшись з розробником бота @MSerega", reply_markup=kb.back_btn)
    await FSM_services.business_center_transport.set()
