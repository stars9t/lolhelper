from peewee import (
    SqliteDatabase,
    DoesNotExist,
    Model
)

from typing import Union

from logs import logger
from exceptions import base_exception
from config import DATABASE
from models import Champion, ChampionLink
from processing import runes_to_text, items_to_text


database = SqliteDatabase(DATABASE)


@base_exception
def get_link_name(name: str) -> Union[Model, bool]:
    """
    Translate ru name champion to english for searching champion in
    website with http request.
    """
    try: 
        database.connect()
        champion_link = ChampionLink.get(russian_name=name)
        return champion_link.link_name
    except DoesNotExist:
        try:
            champion_link = ChampionLink.get(link_name=name)
        except DoesNotExist:
            return False
    finally:
        database.close()


def upsert_champion_info(info: dict, link_name: str) -> bool:
    """
    Insert new champion in database. When champion is 
    in the base - rewrite this champion.
    """
    try:
        database.connect()
        new_champion = Champion.insert(
            link_name = link_name,
            name = info['name'],
            roles = items_to_text(info['roles']), 
            core_weapons = items_to_text(info['core_weapons']),
            late_weapons = items_to_text(info['late_weapons']),
            strong_against = items_to_text(info['strong_against']),
            weak_against = items_to_text(info['weak_against']),
            core_runes = runes_to_text(info['core_runes']),
            extra_runes = runes_to_text(info['extra_runes'])
        ).on_conflict_replace().execute()
        return True
    except Exception as e:
        logger.warning(f"DB!{__name__}: {e}")
        return False
    finally:
        database.close()


@base_exception
def get_champion_db(link_name: str) -> Union[Model, bool]:
    """
    Get champion from database(cache).
    """
    try:
        database.connect()
        champion = Champion.get(link_name=link_name)
        return champion
    except DoesNotExist:
        return False
    except Exception as e:
        logger.warning(f"DB!{__name__}: {e}")
    finally:
        database.close()
    