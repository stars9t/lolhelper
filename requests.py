import functools
import re
from typing import Dict, List

import urllib3
from bs4 import BeautifulSoup
from urllib3 import HTTPResponse

import config
from logs import logger


http = urllib3.PoolManager()

def base_exception(fn):
    """Standart decorator for except all exceptions"""
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f'Ошибка парсинга, {__name__}: {e}')
    return inner


@base_exception
def request_champion_info(champion: str) -> HTTPResponse:
    """Get http request to website with all statistics about a
    champion with html format"""
    request = http.request(
        'GET',
        f'https://www.leaguespy.gg/league-of-legends/champion/{champion}/stats', 
        None, 
        config.headers
    )

    return request


@base_exception
def get_champion_info(request: HTTPResponse) -> Dict:
    """Get all information about a champion """
    data = BeautifulSoup(request.data, 'lxml')

    champion_information = {
        'name': get_champion_name(data),
        'roles': get_champion_role(data),
        'core_weapons': get_core_weapons(data),
        'late_weapons': get_late_weapons(data),
        'strong_against': get_against(data, 'strong'),
        'weak_against': get_against(data, 'weak'),
        'core_runes': get_core_runes(data),
        'extra_runes': get_extra_runes(data),
    }

    return champion_information


@base_exception
def get_champion_name(data: BeautifulSoup) -> str:
    """Get champion's name"""
    champion_info = data.find('div',
        class_='champ__header__left__main')
    champion_name = champion_info.find('h2').get_text()

    return champion_name


@base_exception
def get_champion_role(data: BeautifulSoup) -> List:
    """Get champion's role or roles if multiple"""
    champions_status = data.find('span', class_='stat-source')
    roles_stack = champions_status.find_all('span',
        class_='stat-source__btn', limit=3)
    roles = []
    for role in roles_stack:
        roles.append(role.get_text())

    return roles


@base_exception
def get_core_weapons(data: BeautifulSoup) -> List:
    """Get core weapons for the champion"""
    core_items_stack = data.find('div', class_='item-block--crossover')
    core_items_img = core_items_stack.find_all('img', alt=True)
    core_items = []

    for img in core_items_img:
        core_items.append(img['alt'])

    return core_items
    
    
@base_exception
def get_late_weapons(data: BeautifulSoup) -> List:
    """Get late weapons for the champion."""
    late_items_stack = data.find_all('div',
        class_='item-block__top item-block__top--inline block-luxury')
    late_items = []
    
    for item in late_items_stack:
        item = item.find('img', alt=True)['alt']
        late_items.append(item)

    return late_items


@base_exception
def get_against(data: BeautifulSoup, power: str) -> List:
    """Get the names of champions who are
    stronger(power=strong) or weaker(power=weak)"""
    if power == 'strong':
        champions_stack = data.find_all('i', 'img-wrap border-2', limit=5)
    elif power == 'weak':
        champions_stack = data.find_all('i', 'img-wrap border-2', limit=10)[5:]
    else:
        raise ValueError('branch not weak or strong')

    champions = []
    for champ in champions_stack:
        name = champ.find('img', alt=True)['alt']
        name = name.split(' ')[0]
        champions.append(name)
    
    return champions 


@base_exception
def get_core_runes(data: BeautifulSoup) -> Dict:
    """Get core runes for the champion.
    First element in dict is name of branch for runes.
    Second element is list for runes."""
    finded_runes = data.find('div', class_='rune-block rune-block--new')
    runes_stack = finded_runes.find_all('span', limit=5)
    core_runes = {'branch_name': runes_stack[0].get_text()}

    runes = []
    for i in runes_stack[1:]:
        runes.append(i.get_text())

    core_runes['runes'] = runes

    return core_runes 


@base_exception
def get_extra_runes(data: BeautifulSoup) -> Dict:
    """Get extra runes for champion. First element in dict
    is name of branch for runes. Second element is list of
    runes."""
    all_runes = data.find('div', class_='rune-block rune-block--new')
    extra_runes_stack = all_runes.find_all('span', limit=8)[5:]
    extra_runes = {'branch_name': extra_runes_stack[0].get_text()}

    runes = []
    for i in extra_runes_stack[1:]:
        runes.append(i.get_text())

    extra_runes['runes'] = runes
    
    return extra_runes
    

@base_exception
def get_all_information(champion: str) -> Dict:
    """Helper function to reqiest and retrieve all
    information about a champion."""
    request = request_champion_info(champion)
    champion_info = get_champion_info(request)

    return champion_info
