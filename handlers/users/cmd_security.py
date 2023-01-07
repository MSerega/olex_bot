from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from loader import dp
from keyboards import default as kb
from settings import functions


class FSM_security(StatesGroup):
    security = State()
    nezlamnist = State()
    fireline = State()


@dp.message_handler(text="🛡 Безпека", chat_type=types.ChatType.PRIVATE, state="*")
async def cmd_poshta(message: types.Message):
    await functions.userInDb(message)
    await FSM_security.security.set()
    await message.answer("Оберіть пункт меню",
                         reply_markup=kb.security_menu,
                         disable_notification=True)


@dp.message_handler(Text(equals="👈️ Назад"), state=FSM_security)
async def back_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_ = current_state.split(':')[1]
    if state_ in ['nezlamnist', 'fireline']:
        await FSM_security.security.set()
        await message.answer("Оберіть пункт меню", reply_markup=kb.security_menu)
    elif state_ == 'security':
        if current_state is None:
            return
        await state.finish()
        await message.answer("Ви в головному меню. Оберіть пункт меню", reply_markup=kb.main_menu)


@dp.message_handler(Text(equals="🏨 Пункти незламності"), state=FSM_security.security)
async def points_nezlamnist(message: types.Message, state: FSMContext):
    await message.answer(
        f"<b>На території громади визначено місця розташування стаціонарних пунктів обігріву ‟Пункти незламності” в приміщеннях:</b>\n\n "

        f"КУ ‟Олександрівський центр соціального обслуговування (надання соціальних послуг)” Олександрівської селищної ради, за адресою: смт Олександрівка, вул. Незалежності України, 47;\n\n"
        f"✅ Генератор\n❌ Булер'ян\n✅ Твердопаливний котел\n✅ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"КЗ ‟Центр культури та дозвілля” Олександрівської селищної ради, за адресою: смт Олександрівка, вул. Коцюбинського, 2;\n\n"
        f"✅ Генератор\n✅ Булер'ян\n❌ Твердопаливний котел\n✅ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"Відділ поліції №1 (м.Знам’янка) Кропивницького районного управління поліції ГУНП України в Кіровоградській області, за адресою: смт Олександрівка, вул Шевченка,2;\n\n"
        f"✅ Генератор\n❌ Булер'ян\n❌ Твердопаливний котел\n❌ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"29-ДПРЧ 1ДПРЗ ГУ ДСНС України у Кіровоградській області, за адресою: смт Олександрівка, вул. Гагаріна,49\n\n"
        f"✅ Генератор\n❌ Булер'ян\n✅ Твердопаливний котел\n✅ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"КНП ‟Олександрівська лікарня”, за адресою: смт.Олександрівка, вул.Шевченка, 57\n\n"
        f"✅ Генератор\n❌ Булер'ян\n✅ Твердопаливний котел\n✅ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"Мобільний пункт ДСНС, за адресою: смт Олександрівка, вул. Незалежності України, 81\n\n"
        f"✅ Генератор\n❌ Булер'ян\n❌ Твердопаливний котел\n❌ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"Пукт незламності відповідального бізнесу: АЗК, за адресою: смт Олександрівка, вул. Незалежності України, 1\n\n"
        f"✅ Генератор\n❌ Булер'ян\n❌ Твердопаливний котел\n❌ Інтернет\n✅ Підзарядка гаджетів\n\n"

        f"<b>Інші пункти незламності Олександрівської громади:</b>\n\n"

        f"КЗ ‟Михайлівський ліцей” Олександрівської селищної ради, за адресою: с Михайлівка, вул. Пушкіна, 1;\n\n"
        f"Староосотської філії КЗ ‟Олександрівський ліцей № 1” Олександрівської селищної ради, за адресою: с Стара Осота, вул. Івана Лісняка, 30;\n\n"
        f"Цвітненської філії КЗ ‟Красносільський ліцей” Олександрівської селищної ради, за адресою: с Цвітне, вул. Шкільна 1;\n\n"
        f"КЗ ‟Красносільський ліцей” Олександрівської селищної ради, за адресою: с Красносілля, вул. Нова 12;\n\n"
        f"Вищеверищаківської філії КЗ ‟Красносільський ліцей” Олександрівської селищної ради, за адресою: с Вищі Верещаки, вул. Шкільна 1;\n\n"
        f"Адміністративне приміщення Бірчанського старостату, за адресою: с Бірки, вул. Центральна 47;\n\n"
        f"Підлісненської філії КЗ ‟Олександрівський ліцей № 2” Олександрівської селищної ради, за адресою: с Підлісне, вул. Авдієвського 1;\n\n"
        f"Лісівської філії КЗ ‟Михайлівський ліцей” Олександрівської селищної ради, за адресою: смт Лісове, вул. Тітова 215;\n\n"
        f"Івангородської філії КЗ ‟Олександрівський ліцей № 2” Олександрівської селищної ради, за адресою: с Івангород, вул. Шкільна 1;\n\n"
        f"Єлизаветградківський заклад дошкільної освіти (дитячий садочок) Олександрівської селищної ради, за адресою: смт Єлизаветградка, пров. Олександра Шаповала 1.\n\n" + kb.links
        , disable_notification=True, reply_markup=kb.back_btn)
    await FSM_security.nezlamnist.set()


@dp.message_handler(Text(equals="🔥 Гаряча лінія"), state=FSM_security.security)
async def points_nezlamnist(message: types.Message, state: FSMContext):
    await message.answer(
        f"Гаряча лінія для всіх жителів Олександрівської селищної територіальної громади.\n\nПо всім питанням просимо "
        f"телефонувати за номерам, який працює цілодобово:\n\n📱 +38(098)-717-72-34.",
        disable_notification=True, reply_markup=kb.back_btn)
    await FSM_security.fireline.set()
