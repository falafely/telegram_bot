from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('Помощь')
b2 = KeyboardButton('Курс BTC')
b3 = KeyboardButton('ChatGPT')
b4 = KeyboardButton('Демотиватор')
b5 = KeyboardButton('Анекдот')

reply_kb.row(b1).add(b2, b3, b4, b5)