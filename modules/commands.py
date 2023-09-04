import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from modules import course
from keyboards.inline_keyboard import kb
from keyboards.keyboard import reply_kb, exit_button
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from create_bot import dp, bot
from modules import demotivator
from modules import gpt
import openai

load_dotenv(find_dotenv())  # поиск файла .env в директории проекта


@dp.message_handler(commands=['start'])
async def start_mes(message: types.Message):
    await bot.send_sticker(message.chat.id, 'Привет!(⌒‿⌒)\n'
                                            'Я фалафелус - самый многофункциональный бот телеграма\n'
                                            'Чтобы ознакомиться со списком команд, напиши /help')
    await message.delete()


@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def help_mes(message: types.Message):
    await bot.send_sticker(message.chat.id,
                           sticker='CAACAgIAAxkBAALtcmTzUniQdE7TraktSzEHhlhWbXEmAALCNgACpj-ZS0ttbatkg_NgMAQ',
                           reply_markup=reply_kb)
    await bot.send_message(message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb,)


# ==============================================================


# ChatGPT
class FSMchatgpt(StatesGroup):
    answer = State()


@dp.message_handler(Text(equals='ChatGPT'), state=None)
@dp.message_handler(commands=['чат'])
async def start_gpt(message: types.Message, state: FSMContext):
    await message.reply('Жду ваш вопрос, хозяин! ♡( ◡‿◡ )', reply_markup=exit_button)
    await state.set_state(FSMchatgpt.answer)


@dp.message_handler(state=FSMchatgpt.answer)
async def chatgpt_mes(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.reply('Как скажешь (¬_¬ )', reply_markup=reply_kb)
        await state.finish()
        return 0
    response = await gpt.chatgpt_mes(message.text)
    await message.reply(response, reply_markup=reply_kb)
    await state.finish()


@dp.callback_query_handler(text='ChatGPT')
async def chatgpt_call(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '<b>ChatGPT</b>\n'
                                                  'Нажимая эту кнопку, ты получаешь эксклюзивную '
                                                  'возможность пообщаться с гуру всех мастей - '
                                                  'Чатом GPT\n(o´▽`o)', parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()

# -------------------------------------------------------

# Демотиватор
class FSMdemotivator(StatesGroup):
    photo = State()
    desc_frst = State()
    desc_sec = State()


@dp.message_handler(Text(equals='Демотиватор', ignore_case=True))
@dp.message_handler(Command("demotivator"), state=None)
async def demotivator_mes(message: types.Message, state: FSMContext):
    await message.reply('Загрузите фото', reply_markup=exit_button)
    await FSMdemotivator.photo.set()


@dp.message_handler(content_types=['photo'], state=FSMdemotivator.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.reply('Как скажешь (¬_¬ )', reply_markup=reply_kb)
        await state.finish()
        return 0
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.photo[-1].download('demotivator.jpg')
    await FSMdemotivator.next()
    await message.reply('Отлично! Теперь введите надпись')


@dp.message_handler(state=FSMdemotivator.desc_frst)
async def load_desc(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.reply('Как скажешь (¬_¬ )', reply_markup=reply_kb)
        await state.finish()
        return 0
    async with state.proxy() as data:
        data['desc_frst'] = message.text
    await FSMdemotivator.next()
    await message.reply('Чилл! Теперь вторая строчка')


@dp.message_handler(state=FSMdemotivator.desc_sec)
async def load_desc_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc_sec'] = message.text
    await FSMdemotivator.next()
    await demotivator.create_demot(user_photo='demotivator.jpg', user_text_frst=data['desc_frst'],
                                   user_text_sec=data['desc_sec'])
    photo = InputFile('demotivator.png')
    await message.reply('Твой демотиватор готов')
    await bot.send_photo(message.chat.id, photo, reply_markup=reply_kb)

    await state.finish()


@dp.callback_query_handler(text='Демотиватор')
async def demot_call(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '<b>Демотиватор</b>\n'
                                                  'Эта функция потребует от тебя фото и подписи к ней,'
                                                  'а взамен ты получаешь лучший демотиватор на просторах '
                                                  'всего телеграма\n'
                                                  '(ღ˘⌣˘ღ)',
                           parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------

# Курс BTC
@dp.message_handler(commands=['course'])
@dp.message_handler(Text(equals='Курс BTC', ignore_case=True))
async def course_mes(message: types.Message):
    now = datetime.now()
    await bot.send_message(message.chat.id, f'-----{now.strftime("%d-%m-%Y | %H:%M:%S")}-----\n'
                                                 f'Курс BTC - {course.btc()}')


@dp.callback_query_handler(text='Курс BTC')
async def course_call(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '<b>Курс BTC</b>\n'
                                                  'Эта команда позволяет ознакомиться с курсом Bitcoin на момент '
                                                  'отправки сообщения в рублях\n'
                                                  'Чтобы использовать нажмите на соответствующую кнопку или введите '
                                                  '/course, чтобы узнать, насколько вы разбогатели\n'
                                                  '(▽◕ ᴥ ◕▽)',
                           parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------

# Анекдот
@dp.message_handler(Text(equals='Анекдот', ignore_case=True))
async def anecdote_mes(message: types.Message):
    await message.answer('Don\'t work')


@dp.callback_query_handler(text='Анекдот')
async def anecdote_call(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '<b>Анекдот</b>\n'
                                                  'Функция, отправляющая абсолютно рандомный анекдот '
                                                  'из своей базы данных\n\n'
                                                  '<b>!(WARNING)!</b>\n\n'
                                                  'В данный момент функция не работает, но автор делает '
                                                  'все, что в его силах, чтобы это исправить!\n'
                                                  '(っ˘ڡ˘ς)',
                           parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------

# Перевод гс
@dp.callback_query_handler(text='Перевод гс')
async def translate_call(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '<b>Переводчик</b>\n'
                                                  'При запуске этой функции бот потребует от тебя голосовое, '
                                                  'которое он конвертирует в текст благодаря своим '
                                                  'межгалактичеким алгоритмам\n'
                                                  '(´ ∀ ` *)',
                           parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------

# echo
@dp.message_handler()
async def echo(message: types.Message):
    pass


# ==============================================================

def reg_mod(dp: Dispatcher):
    dp.register_message_handler(start_mes, commands=['start'])
    dp.register_message_handler(start_gpt, commands=['чат'])
    dp.register_message_handler(demotivator_mes, state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMContext)
    dp.register_message_handler(load_desc, state=FSMContext)
    dp.register_message_handler(load_desc_2, state=FSMContext)
    dp.register_message_handler(echo)
