from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb = InlineKeyboardMarkup(row_width=2)

bt1 = InlineKeyboardButton(text='ChatGPT', callback_data='ChatGPT')
bt2 = InlineKeyboardButton(text='Демотиватор', callback_data='Демотиватор')
bt3 = InlineKeyboardButton(text='Курс BTC', callback_data='Курс BTC')
bt4 = InlineKeyboardButton(text='Анекдот', callback_data='Анекдот')
bt5 = InlineKeyboardButton(text='Перевод гс', callback_data='Перевод гс')
author = InlineKeyboardButton(text='Автор', url='https://t.me/falafelyy')

kb.add(bt1, bt2, bt3, bt4, bt5).add(author)