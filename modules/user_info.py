from aiogram import types
from datetime import datetime


def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_text = message.text
    mes_time = datetime.now()
    with open('users.txt', 'a') as file:
        file.write(f'\n==================================\n'
                   f'ID - {user_id}\n'
                   f'NAME - @{user_name}\n'
                   f'TEXT - {user_text}\n'
                   f'{mes_time}\n'
                   f'==================================\n')
