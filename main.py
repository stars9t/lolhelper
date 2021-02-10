from aiogram import Bot, Dispatcher, executor, types

from config import API_TOKEN
from db import get_translated_name
from processing import message_pretify
from requests import get_all_champion_info
from exceptions import base_exception


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@base_exception
@dp.message_handler()
async def champion_info(message: types.Message) -> None:
    """
    Send information about champion.
    """
    champion = get_translated_name(message.text.lower())

    if champion:
        #link is column in model
        champion_info = get_all_champion_info(champion.link)
        msg = message_pretify(champion_info)
        await message.answer(msg)
    else:
        await message.answer('Такого персонажа не существует')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)