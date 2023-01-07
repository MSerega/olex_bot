import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from loader import dp
from settings.config import ADMIN
import keyboards as kb
from settings.functions import userInDb


class FSMAdmin(StatesGroup):
    screen_pay = State()
    ads_text = State()


@dp.message_handler(commands=['advertising'], chat_type=types.ChatType.PRIVATE, state="*")
async def advertising(message: types.Message):
    await userInDb(message)
    await message.answer("Якщо ви бажаєте, щоб ваше комерційне оголошення (куплю/продам/послуги) "
                         "було опубліковане в групі чи каналі - прошу попередньо, перерахувати 80 грн на розвиток "
                         "групи",
                         reply_markup=kb.inline.advertising, disable_notification=True)

    await asyncio.sleep(3)
    await FSMAdmin.screen_pay.set()
    await message.answer("Завантажте скріншот про успішну оплату оголошення",
                         reply_markup=kb.default.cancel_fsm, disable_notification=True)


@dp.message_handler(Text(equals="📤 Скасувати"), state=FSMAdmin)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ви скасували процедуру оформлення рекламного оголошення",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], state=FSMAdmin.screen_pay)
async def screen_pay(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['photo_id'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Напишіть рекламне оголошення", reply_markup=kb.default.cancel_fsm, disable_notification=True)


@dp.message_handler(state=FSMAdmin.ads_text)
async def text_of_advertising(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ads_text'] = message.text
    await state.finish()
    await message.answer("Як тільки модератор перевірить оплату, ваше оголошення буде опубліковано в групі та каналі", disable_notification=True)

    kb_contact = types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton("✉ Зв'язатись з автором", url=f"tg://user?id={data['user_id']}"))

    await dp.bot.send_photo(ADMIN, data['photo_id'], caption=f"{data['ads_text']}", reply_markup=kb_contact)
