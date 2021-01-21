from aiogram import Bot, Dispatcher, executor, types

import config
from db import get_translated_name
from logs import logger
from processing import message_pretify
from requests import get_all_information


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def champion_info(message: types.Message) -> None:
    logger.info(f'{message.text}')
    champion = get_translated_name(message.text.lower())

    if champion == None:
        await message.answer('Такого чемпиона не существует')
    else:
        try:
            champion_info = get_all_information(champion)
            msg = message_pretify(champion_info)
        except Exception as e:
            logger.warning(f'{__name__}: {e}')
            msg = 'Произошла ошибка на стороне сервера'
        await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)