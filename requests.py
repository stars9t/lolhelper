import urllib3
from bs4 import BeautifulSoup
from urllib3 import HTTPResponse

from config import HEADERS
from exceptions import base_exception 
from parsing import (
    parse_champion_name,
    parse_champion_role,
    parse_core_runes,
    parse_core_weapons,
    parse_extra_runes,
    parse_late_weapons,
    parse_other_champions
)


http = urllib3.PoolManager()


@base_exception
def request_champion(champion_name: str) -> BeautifulSoup:
    """
    Get http request to website with all statistics about a
    champion with html format.
    """
    request = http.request(
        'GET',
        f'https://www.leaguespy.gg/league-of-legends/champion/{champion_name}/stats', 
        None, 
        HEADERS

    )

    return BeautifulSoup(request.data, 'lxml')


@base_exception
def get_all_champion_info(champion_name: str) -> dict:
    """
    Get all information about a champion.
    """
    data = request_champion(champion_name)

    info = {
        'name': parse_champion_name(data),
        'roles': parse_champion_role(data),
        'core_weapons': parse_core_weapons(data),
        'late_weapons': parse_late_weapons(data),
        'strong_against': parse_other_champions(data, 'strong'),
        'weak_against': parse_other_champions(data, 'weak'),
        'core_runes': parse_core_runes(data),
        'extra_runes': parse_extra_runes(data),
    }

    return info
    