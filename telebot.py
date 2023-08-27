from aiogram.utils import executor
from create_bot import dp
from modules import commands, demotivator, gpt


async def on_startup(_):
    print('=================\n'
          'Бот онлайн...\n'
          '=================')

gpt.gpt_reg_mod(dp)
commands.reg_mod(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
