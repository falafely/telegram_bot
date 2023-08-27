from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from modules import course
from keyboards.inline_keyboard import kb
from keyboards.keyboard import reply_kb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from create_bot import dp, bot
from modules import demotivator
from modules import gpt

load_dotenv(find_dotenv())  # поиск файла .env в директории проекта


@dp.message_handler(commands=['start'])
async def start_mes(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я фалафелус - самый многофункциональный бот телеграма\n'
                                                 'Чтобы ознакомиться со списком команд, напиши /help')
    await message.delete()


@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def help_mes(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEKItFk6lTqBc5NiBRFHq5WXbe_Gmct6AACriEAAjNY0UqtYYJRFpNzDjAE',
                           reply_markup=reply_kb)
    await bot.send_message(message.from_user.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )


# ==============================================================

# ChatGPT
# class FSMchatgpt(StatesGroup):
#     chat = State()
#
#
# @dp.message_handler(Text(equals='📌📌📌🌐ChatGPT', ignore_case=True), state=None)
# async def chatgpt_mes(message: types.Message):
#     await message.reply('<b>Вы вошли в чат с ChatGPT</b>\n'
#                         'Задайте свой вопрос', parse_mode='HTML')
#     await FSMchatgpt.chat.set()
#
#
# @dp.message_handler(state=FSMchatgpt.chat)
# async def load_gpt_mes(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['chat'] = message.text
#     answer = gpt.chatgpt_mes(message.text)
#     await bot.send_message(message.from_user.id, answer)
#
#     await state.finish()
#
#
@dp.callback_query_handler(text='ChatGPT')
async def chatgpt_call(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '<b>ChatGPT</b>\n'
                                                  'С помощью этой команды ты попадаешь в диалог со взезнающем гуру - ChatGPT!\n'
                                                  'Ты будешь находиться в чате, пока не нажмешь кнопку "Отмена", '
                                                  'появившуюся после входа в диалог.\n\n'
                                                  '<b>!(WARNING)!</b>\n\n'
                                                  'Пока что бот не запоминает историю переписки, '
                                                  'но автор упорно работает над этим ♡( ◡‿◡ )', parse_mode='HTML')
    await bot.send_message(callback.from_user.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------


# Демотиватор
class FSMdemotivator(StatesGroup):
    photo = State()
    desc = State()


@dp.message_handler(Text(equals='Демотиватор', ignore_case=True))
@dp.message_handler(Command("demotivator"), state=None)
async def demotivator_mes(message: types.Message):
    await message.reply('Загрузите фото')
    await FSMdemotivator.photo.set()


@dp.message_handler(content_types=['photo'], state=FSMdemotivator.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.photo[-1].download('demotivator.jpg')
    await FSMdemotivator.next()
    await message.reply('Отлично! Теперь введите надпись')


@dp.message_handler(state=FSMdemotivator.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await demotivator.create_demot(user_photo='demotivator.jpg', user_text=message.text)
    photo = InputFile('demotivator.jpg')
    await bot.send_message(message.from_user.id, 'Вот твой демотиватор')
    await bot.send_photo(message.from_user.id, photo=photo)

    await state.finish()


@dp.callback_query_handler(text='Демотиватор')
async def demot_call(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '</b>Демотиватор</b>\n'
                                                  'Эта функция потребует от тебя фото и подписи к ней,'
                                                  'но взамен ты получаешь демотиватор, который создал ты сам! '
                                                  '(ღ˘⌣˘ღ)', parse_mode='HTML')
    await bot.send_message(callback.from_user.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb, )
    await callback.answer()


# -------------------------------------------------------

# Курс BTC
@dp.message_handler(commands=['course'])
@dp.message_handler(Text(equals='Курс BTC', ignore_case=True))
async def course_mes(message: types.Message):
    now = datetime.now()
    await bot.send_message(message.from_user.id, f'-----{now.strftime("%d-%m-%Y %H:%M:%S")}-----\n'
                                                 f'Курс BTC - {course.btc()}')


@dp.callback_query_handler(text='Курс BTC')
async def course_call(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '<b>Курс BTC</b>\n'
                                                  'Эта команда позволяет ознакомиться с курсом Bitcoin на момент '
                                                  'отправки сообщения в рублях\n'
                                                  'Чтобы использовать нажмите на соответствующую кнопку или введите '
                                                  '/course, чтобы узнать, насколько вы разбогатели ＼(￣▽￣)／',
                           parse_mode='HTML')
    await bot.send_message(callback.from_user.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb,)
    await callback.answer()


# -------------------------------------------------------

# Анекдот
@dp.message_handler(Text(equals='Анекдот', ignore_case=True))
async def anecdote_mes(message: types.Message):
    await message.answer('Don\'t work')


@dp.callback_query_handler(text='Анекдот')
async def anecdote_call(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '<b>Анекдот</b>\n'
                                                  'Функция, отправляющая абсолютно рандомный анекдот '
                                                  'из своей базы данных\n\n'
                                                  '<b>!(WARNING)!</b>\n\n'
                                                  'В данный момент функция не работает, но автор делает '
                                                  'все, что в его силах, чтобы это исправить! (っ˘ڡ˘ς)',
                           parse_mode='HTML')
    await bot.send_message(callback.from_user.id, 'Нажмите, чтобы ознакомиться с кратким описание функции',
                           reply_markup=kb,)
    await callback.answer()


# -------------------------------------------------------

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Вы не ввели команды')


# ==============================================================

def reg_mod(dp: Dispatcher):
    dp.register_message_handler(start_mes, commands=['start'])
    dp.register_message_handler(demotivator_mes, state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMContext)
    dp.register_message_handler(load_desc, state=FSMContext)
    dp.register_message_handler(echo)
