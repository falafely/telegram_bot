from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('Помощь')
b2 = KeyboardButton('ChatGPT')
b3 = KeyboardButton('Демотиватор')
b4 = KeyboardButton('Курс BTC')
b5 = KeyboardButton('Анекдот')
b6 = KeyboardButton('Перевод гс')

reply_kb.row(b1).add(b2, b3, b4, b5, b6)


exit_button = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
exit = KeyboardButton('Отмена')
exit_button.add(exit)