from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

advertising = InlineKeyboardMarkup().row(InlineKeyboardButton("💶 Оплатити", url="https://privatbank.ua/ru/sendmoney?payment=b668b42f51"))
light = InlineKeyboardMarkup().row(InlineKeyboardButton("🕰 Графік відключень", url="https://kiroe.com.ua/energy/emergency"))