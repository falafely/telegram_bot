from keyboards.inline_keyboard import kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
import os
import openai
from aiogram import types, Dispatcher
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # поиск файла .env в директории проекта


async def chatgpt_mes(message: types.Message):
    openai.api_key = (os.getenv('GPT_TOKEN'))
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.0,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    answer = response['choices'][0]['text']
    return answer


class FSMchatgpt(StatesGroup):
    chat = State()


@dp.message_handler(Text(equals='📌📌📌🌐ChatGPT', ignore_case=True), state=None)
async def chatgpt_mes(message: types.Message):
    await message.reply('<b>Вы вошли в чат с ChatGPT</b>\n'
                        'Задайте свой вопрос', parse_mode='HTML')
    await FSMchatgpt.chat.set()


@dp.message_handler(state=FSMchatgpt.chat)
async def load_gpt_mes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat'] = message.text
    answer = chatgpt_mes(message.text)
    await bot.send_message(message.from_user.id, answer)

    await state.finish()


def gpt_reg_mod(dp: Dispatcher):
    dp.register_message_handler(chatgpt_mes, state=None)
    dp.register_message_handler(load_gpt_mes, state=FSMContext)