import asyncio

from db import upsert_champion_info, get_all_champions_links
from exceptions import base_exception
from requests import get_all_champion_info
from logs import logger


@base_exception
async def update_database(update_period: int, insertion_period: int,
                               log: bool = False) -> None:
    """
    We update the database, as information about characters changes
    from time to time.

    :param update_period: Time in hours after which the database
    will be updated. Minimum 24 hours
    
    :param insertion_period: Time in seconds after which the
    request to the site will occur. Minimum 15 seconds

    :param log: Whether to write data about character
    insertion into the logs. False by default
    """
    
    while True:
        logger.info(f"{__name__}: Start updating database")
        champions = get_all_champions_links()

        if champions:
            for link_name in champions:
                champion_info = get_all_champion_info(link_name)
                status = upsert_champion_info(champion_info, link_name)
                if insertion_period < 15:
                    insertion_period = 15
                if log:
                    logger.info(f"{__name__} - insert champion {link_name}")
                await asyncio.sleep(insertion_period)

        update_period *= 3600
        if update_period < 24:
            update_period = 24

        await asyncio.sleep(update_period)
