from aiogram.types import ReplyKeyboardMarkup

links = '\n\n<a href="https://t.me/olexandrivka">✏ Наш канал</a>' \
        ' <a href="https://t.me/olexandrivka_chat">👩‍👦‍👦 Cпільнота</a>' \
        '\n<a href="https://t.me/olexandrivka_bot?start=news">🧾 Запропонувати новину</a>' \
        '\n<a href="https://t.me/olexandrivka_bot?start=advertising">💶 Замовити рекламу</a>'

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚨 Мапа тривог', '🛡 Безпека') \
    .row("🚌 Транспорт", '💵 Курс валют') \
    .row('🌤 Погода', '🚚 Пошта')

transport_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚕 Таксі', '🚌 Автобуси', '🚋 Поїзди').row('👈️ Назад')

back_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('👈️ Назад')

cancel_fsm = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add('📤 Скасувати')

poshta = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚚 Укрпошта', '🚚 Нова Пошта').row('👈️ Назад')

novaposhta = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🗓 Графік роботи').row('📦 Відділення №1', '📦 Відділення №2').row('👈️ Назад')

ukrposhta = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🗓 Графік роботи', '📦 Відділення').row('👈️ Назад')

security_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🔥 Гаряча лінія').row('🏨 Пункти незламності').row('👈️ Назад')

trains_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚞 Приміські поїзди').row('👈️ Назад')
