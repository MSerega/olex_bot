from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from keyboards import default as kb
from .states_services import FSM_services


@dp.message_handler(Text(equals="🌐 Інтернет"), state=FSM_services.services)
async def cmd_providers(message: types.Message, state: FSMContext):
    await message.answer("Оберіть інтернет провайдера", reply_markup=kb.internetProviders)
    await FSM_services.internet_providers.set()


@dp.message_handler(Text(equals="📶 HomeNet"), state=FSM_services.internet_providers)
async def cmd_home_net(message: types.Message, state: FSMContext):
    await message.answer("Для підключення інтернету від провайдера \"HomeNet\" "
                         "зателефонуйте за номером:\n📱 +38(067)-408-18-58", reply_markup=kb.back_btn)
    await FSM_services.homeNet.set()


@dp.message_handler(Text(equals="📶 SvitNet"), state=FSM_services.internet_providers)
async def cmd_svit_net(message: types.Message, state: FSMContext):
    await message.answer("Для підключення інтернету від провайдера \"SvitNet\" "
                         "зателефонуйте за номером:\n📱 +38(068)-881-62-04", reply_markup=kb.back_btn)
    await FSM_services.svitNet.set()
