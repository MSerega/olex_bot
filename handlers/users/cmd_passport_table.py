from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp
from keyboards import default as kb
from .states_services import FSM_services


@dp.message_handler(Text(equals="🧧 Паспортний стіл"), state=FSM_services.services)
async def cmd_passport_table(message: types.Message, state: FSMContext):
    await FSM_services.passport_table.set()

    await message.answer(
        "<b>Олександрівський районний сектор управління державної міграційної служби України у Кіровоградській області</b>"
        "\n\nКод підрозділу: 3514"
        "\nШифр підрозділу (для платіжних реквізитів): 423507"
        "\nТелефон: +38(05242)3-28-14\n\n"
        "<b>Графік роботи:</b>\n\n"
        "🕰 понеділок: вихідний\n"
        "🕰 вівторок: 08:00-17:00\n"
        "🍽 Обідня перерва: 12:00-12:45\n\n"
        "🕰 середа: 09:00-18:00\n"
        "🍽 Обідня перерва: 12:00-12:45\n\n"
        "🕰 четвер: 08:00-17:00\n"
        "🍽 Обідня перерва: 12:00-12:45\n\n"
        "🕰 п`ятниця: 09:00-18:00\n"
        "🍽 Обідня перерва: 12:00-12:45\n\n"
        "🕰 субота: 08:00-15:45\n"
        "🍽 Обідня перерва: 12:00-12:45\n\n"
        "🕰 неділя: вихідний", reply_markup=kb.back_btn)
