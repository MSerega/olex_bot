import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from keyboards import default as kb
from .states_services import FSM_services
from db.db_connect import insurance_auto


@dp.message_handler(Text(equals="🚘 Cтрахування"), state=FSM_services.services)
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