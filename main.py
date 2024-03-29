from aiogram import Bot, Dispatcher, executor, types
import asyncio

from config import API_TOKEN
from db import get_link_name, get_champion_db, upsert_champion_info
from processing import message_prettify
from requests import get_all_champion_info
from exceptions import base_exception
from updater import update_database


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@base_exception
@dp.message_handler()
async def champion_info(message: types.Message) -> None:
    """
    Send information about champion.
    """
    link_name = get_link_name(message.text.lower())

    if link_name:
        champion = get_champion_db(link_name)

        if not champion:
            info = get_all_champion_info(link_name)
            upsert_champion_info(info, link_name)
            champion = get_champion_db(link_name)

        msg = message_prettify(champion)
        await message.answer(msg)
    else:
        await message.answer('Такого персонажа не существует')


if __name__ == '__main__':
    # Create a loop to add an update with time.sleep.
    loop = asyncio.get_event_loop()
    loop.create_task(update_database(168, 30, True))
    # Start bot.
    executor.start_polling(dp, skip_updates=False, loop=loop)
