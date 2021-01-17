from aiogram import Bot, Dispatcher, executor, types
from requests import get_all_information
import config
from logs import logger
from processing import message_pretify
from db import get_translated_name


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def role(message: types.Message):
    
    champion = get_translated_name(message.text.lower())

    if champion == None:
        await message.answer('Такого чемпиона не существует')
    else:
        try:
            champion_info = get_all_information(champion)
            msg = message_pretify(champion_info)
        except:
            msg = 'Произошла ошибка на стороне сервера'
        await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
