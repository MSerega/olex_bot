import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db.db_connect import insurance_auto
from loader import dp, bot
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
    providers_internet = State()
    homeNet = State()
    svitNet = State()


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
    if state_ in ['officeInsurance', 'providers_internet']:
        await FSM_services.services.set()
        await message.answer("Оберіть послугу", reply_markup=kb.services_menu)
    if state_ in ['homeNet', 'svitNet']:
        await FSM_services.providers_internet.set()
        await message.answer("Оберіть провайдера", reply_markup=kb.internetProviders)
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


@dp.message_handler(Text(equals="🚘 Автострахування"), state=FSM_services.services)
async def cmd_insurance(message: types.Message, state: FSMContext):
    await message.answer("Для страхування вашого авто потрібно заповнити наступні дані")
    await asyncio.sleep(1)
    await message.answer("Оберіть страхову компанію, яка оформить вам страховку на ваше авто.",
                         reply_markup=kb.officeInsurance)
    await FSM_services.officeInsurance.set()


@dp.message_handler(Text(equals=['🚗 ТАС']), state=FSM_services.officeInsurance)
async def get_officeInsurance(message: types.Message, state: FSMContext):
    if message.text is not None:
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            if message.text == '🚗 ТАС':
                data['officeInsurance'] = '145333452'
            else:
                data['officeInsurance'] = 'Інша фірма'
        await message.answer("Прикріпіть фото вашого ідентифікаційного коду, так щоб наш менеджер зміг прочитати",
                             reply_markup=kb.cancel_fsm)
        await FSM_services.userCode.set()


@dp.message_handler(content_types=['photo', 'text'], state=FSM_services.userCode)
async def get_userCode(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['userCode'] = message.photo[-1].file_id
        await message.answer("Прикріпіть фото одного з наступних документів:"
                             "\n- посвідчення водія;"
                             "\n- паспорт;"
                             "\n- пенсійне посвідчення пенсійне;"
                             "\n- посвідчення учасника бойових дій (УБД)")
        await FSM_services.driver_passport.set()
    else:
        await message.answer("Ви не завантажили фото. Повторіть спробу")


@dp.message_handler(content_types=['photo', 'text'], state=FSM_services.driver_passport)
async def get_driverPassport(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['driverPassport'] = message.photo[-1].file_id
        await message.answer("Прикріпіть фото <b>першої сторінки</b> технічного паспорту")
        await FSM_services.technical_passport01.set()
    else:
        await message.answer("Ви не завантажили фото. Повторіть спробу")


@dp.message_handler(content_types=['photo', 'text'], state=FSM_services.technical_passport01)
async def get_technicalPassport(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['technicalPassport01'] = message.photo[-1].file_id
        await FSM_services.technical_passport02.set()
        await message.answer("Прикріпіть фото <b>другої сторінки</b> технічного паспорту")
    else:
        await message.answer("Ви не завантажили фото. Повторіть спробу")


@dp.message_handler(content_types=['photo', 'text'], state=FSM_services.technical_passport02)
async def get_technicalPassport(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['technicalPassport02'] = message.photo[-1].file_id
        await FSM_services.phone_ownerCar.set()
        await message.answer("Вкажіть ваш номер мобільного телефону")
    else:
        await message.answer("Ви не завантажили фото. Повторіть спробу")


@dp.message_handler(state=FSM_services.phone_ownerCar)
async def get_phoneOwnerCar(message: types.Message, state: FSMContext):
    if message.text is not None:
        async with state.proxy() as data:
            data['phoneOwnerCar'] = message.text
        await state.finish()
        mediaGroup = types.MediaGroup()
        mediaGroup.attach_photo(data['userCode'], 'Ідентифікаційний код')
        mediaGroup.attach_photo(data['driverPassport'], 'Посвідчення')
        mediaGroup.attach_photo(data['technicalPassport01'], 'Технічний паспорт 1 сторінка')
        mediaGroup.attach_photo(data['technicalPassport02'], 'Технічний паспорт 2 сторінка')
        insurance_auto(data)
        await bot.send_media_group(data['officeInsurance'], media=mediaGroup)
        await bot.send_message(data['officeInsurance'], "Вітаю, у вас є новий клієнт на оформлення страховки.\n"
                                                        "Вище я прикріпив документи, які мені надав власник авто\n"
                                                        f"Ви можете зателефонувати йому за номером: {data['phoneOwnerCar']}")
        await FSM_services.services.set()
        await message.answer("Дякуємо. Ваші дані прийнято в обробку. Чекайте на дзвінок від стахової компанії",
                             reply_markup=kb.services_menu)


@dp.message_handler(Text(equals="🌐 Інтернет"), state=FSM_services.services)
async def cmd_providers(message: types.Message, state: FSMContext):
    await message.answer("Оберіть інтернет провайдера", reply_markup=kb.internetProviders)
    await FSM_services.providers_internet.set()


@dp.message_handler(Text(equals="📶 HomeNet"), state=FSM_services.providers_internet)
async def cmd_insurance(message: types.Message, state: FSMContext):
    await message.answer("Для підключення інтернету від провайдера \"HomeNet\" "
                         "зателефонуйте за номером:\n📱 +38(067)-408-18-58", reply_markup=kb.back_btn)
    await FSM_services.homeNet.set()


@dp.message_handler(Text(equals="📶 SvitNet"), state=FSM_services.providers_internet)
async def cmd_insurance(message: types.Message, state: FSMContext):
    await message.answer("Для підключення інтернету від провайдера \"SvitNet\" "
                         "зателефонуйте за номером:\n📱 +38(068)-881-62-04", reply_markup=kb.back_btn)
    await FSM_services.svitNet.set()
