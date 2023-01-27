from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db.db_connect import get_horoscope
from loader import dp
from keyboards import default as kb
from settings import functions


class FSM_horoscope(StatesGroup):
    horoscope = State()
    prevision = State()


@dp.message_handler(text="♏ Гороскоп", chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_horoscope(message: types.Message):
    await functions.userInDb(message)
    await FSM_horoscope.horoscope.set()
    await message.answer("Оберіть знак зодіака",
                         reply_markup=kb.zodiacs,
                         disable_notification=True)


@dp.message_handler(Text(equals="👈️ Назад"), state=FSM_horoscope)
async def back_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_ = current_state.split(':')[1]
    if state_ == 'prevision':
        await FSM_horoscope.horoscope.set()
        await message.answer("Оберіть знак зодіака", reply_markup=kb.zodiacs)
    elif state_ == 'horoscope':
        if current_state is None:
            return
        await state.finish()
        await message.answer("Ви в головному меню. Оберіть пункт меню", reply_markup=kb.main_menu)


@dp.message_handler(Text(equals=['♈ Овен', '♉ Тілець', '♊ Близнюки', '♋ Рак', '♌ Лев', '♍ Діва', '♎ Терези',
                                 '♏ Скорпіон', '♐ Стрілець', '♑ Козеріг', '♒ Водолій', '♓ Риби']),
                    state=FSM_horoscope.horoscope)
async def zodiacs(message: types.Message, state: FSMContext):
    if '♈ Овен' == message.text:
        oven = get_horoscope('Овен')
        await message.answer(f"♈ Овен, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{oven}",
                             reply_markup=kb.back_btn)
    elif '♉ Тілець' == message.text:
        await message.answer(f"♉ Тілець, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Телець')}",
                             reply_markup=kb.back_btn)
    elif '♊ Близнюки' == message.text:
        await message.answer(f"♊ Близнюки, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Близнюкі')}",
                             reply_markup=kb.back_btn)
    elif '♋ Рак' == message.text:
        await message.answer(f"♋ Рак, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Рак')}",
                             reply_markup=kb.back_btn)
    elif '♌ Лев' == message.text:
        await message.answer(f"♌ Лев, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Лев')}",
                             reply_markup=kb.back_btn)
    elif '♍ Діва' == message.text:
        await message.answer(f"♍ Діва, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Дева')}",
                             reply_markup=kb.back_btn)
    elif '♎ Терези' == message.text:
        await message.answer(f"♎ Терези, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Терези')}",
                             reply_markup=kb.back_btn)
    elif '♏ Скорпіон' == message.text:
        await message.answer(f"♏ Скорпіон, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Скорпіон')}",
                             reply_markup=kb.back_btn)
    elif '♐ Стрілець' == message.text:
        await message.answer(f"♐ Стрілець, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Стрелець')}",
                             reply_markup=kb.back_btn)
    elif '♑ Козеріг' == message.text:
        await message.answer(f"♑ Козеріг, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Козерог')}",
                             reply_markup=kb.back_btn)
    elif '♒ Водолій' == message.text:
        await message.answer(f"♒ Водолій, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Водолей')}",
                             reply_markup=kb.back_btn)
    elif '♓ Риби' == message.text:
        await message.answer(f"♓ Риби, гороскоп на {datetime.now().strftime('%d.%m.%Y')}\n{get_horoscope('Риби')}",
                             reply_markup=kb.back_btn)
    await FSM_horoscope.prevision.set()
