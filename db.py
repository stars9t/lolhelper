from peewee import (
    SqliteDatabase,
    DoesNotExist
)
from typing import Optional

from logs import logger
from requests import base_exception
from config import DATABASE
from models import Champion, ChampionLink


database = SqliteDatabase(DATABASE)

def get_translated_name(name: str) -> Optional[str]:
    """
    Translate ru name champion to english for searching champion in
    website with http request.
    """
    database.connect()
    try: 
        champion_link = ChampionLink.get(russian_name=name)
    except DoesNotExist:
        try:
            champion_link = ChampionLink.get(link=name)
        except DoesNotExist:
            database.close()
            return False
    database.close()
    return champion_link
