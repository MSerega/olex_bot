from aiogram.types import ReplyKeyboardMarkup

links = '\n\n<a href="https://t.me/olexandrivka">✏ Наш канал</a>' \
        ' <a href="https://t.me/olexandrivka_chat">👩‍👦‍👦 Cпільнота</a>' \
        '\n<a href="https://t.me/olexandrivka_bot?start=news">🧾 Запропонувати новину</a>' \
        '\n<a href="https://t.me/olexandrivka_bot?start=advertising">💶 Замовити рекламу</a>'

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚨 Мапа тривог', '🗄 Послуги') \
    .row('🚌 Транспорт', '🚚 Пошта') \
    .row('🌤 Погода', '♏ Гороскоп') \
    .row('💵 Курс валют', '🛡 Безпека')

transport_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚕 Таксі', '🚌 Автобуси', '🚋 Потяги').row('👈️ Назад')

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
    .row('🏫 Заліжничний вокзал').row('🚞 Приміські потяги').row('🚞 Пасажирські потяги').row('👈️ Назад')

zodiacs = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('♈ Овен', '♉ Тілець', '♊ Близнюки') \
    .row('♋ Рак', '♌ Лев', '♍ Діва') \
    .row('♎ Терези', '♏ Скорпіон', '♐ Стрілець') \
    .row('♑ Козеріг', '♒ Водолій', '♓ Риби').row('👈️ Назад')

services_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🎮 Розваги').row('🚘 Автострахування').row('🚑 Медицина', '🌐 Інтернет').row('👈️ Назад')

officeInsurance = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🚗 ТАС').row('👈️ Назад')

internetProviders = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('📶 HomeNet', '📶 SvitNet').row('👈️ Назад')

medicine_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🏥 Лікарня', '🐶 Ветеринари').row('👈️ Назад')

funs_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🏢 Бізнес-центр "Порядок"').row('👈️ Назад')

cmd_business_center_info = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🧾 Послуги', '🗺 Ми на карті').row('👈️ Назад')

cmd_business_center_services = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🙍‍♀ Краса', '❤ Здоров\'я') \
    .row('🕹 Розваги', '🛠 Виробництво') \
    .row('🚛 Перевезення', '👈️ Назад')

cmd_business_center_krasa = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('➡ Манікюр', '➡ Парикмахер').row('➡ Візажист', '👈️ Назад')

cmd_business_center_medicine = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('➡ Масажист', '➡ Стоматолог').row('➡ Косметолог', '👈️ Назад')

cmd_business_center_funs = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row('🎱 Більярд').row('👫 Розважальний центр').row('👈️ Назад')