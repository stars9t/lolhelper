from bs4 import BeautifulSoup
import urllib3 
import config 
from logs import logger
import functools
import re


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
def request_champion_info(champion):
    """Get request and return html code of page about champion"""
    request = http.request(
        'GET',
        f'https://www.leaguespy.gg/league-of-legends/champion/{champion}/stats', 
        None, 
        config.headers
    )

    return request


@base_exception
def get_champion_info(request):
    """Get all info about champion in text format"""
    data = BeautifulSoup(request.data, 'lxml')
    strong_against, weak_against = get_champion_against(data)
    core_runes, extra_runes = get_champion_runes(data)

    all_information = {
        'name': get_champion_name(data),
        'role': get_champion_role(data),
        'base_weapons': get_base_weapons(data),
        'late_weapons': get_late_weapons(data),
        'strong_against': strong_against,
        'weak_against': weak_against,
        'core_runes': core_runes,
        'extra_runes': extra_runes,
    }

    return all_information


@base_exception
def get_champion_name(data):
    """Get champion name. Return string"""
    champion_main = data.find('div',
        class_='champ__header__left__main')
    champion_name = champion_main.find('h2').get_text()

    return champion_name


@base_exception
def get_champion_role(data):
    """Get champion role or roles. Return sting in both cases"""
    stat_role = data.find('span', class_='stat-source')
    champion_roles = stat_role.find_all('span',
        class_='stat-source__btn', limit=3)
    roles = ''
    for i in champion_roles:
        roles += i.get_text() + ', '

    return roles[:-2]


@base_exception
def get_base_weapons(data):
    """Get text about all base weapons for champion"""
    core_items = data.find('div', class_='item-block--crossover')
    two_items = core_items.find_all('img', alt=True)
    output = ''
    for img in two_items:
        output += img['alt'] + '\n'

    return output
    
    
@base_exception
def get_late_weapons(data):
    """Get text about all late weapons for champion"""
    luxury_items = data.find_all('div',
        class_='item-block__top item-block__top--inline block-luxury')
    output = ''
    for item in luxury_items:
        output += item.find('img', alt=True)['alt'] + '\n'

    return output


@base_exception
def get_champion_against(data):
    """Get the name of the champions against which the champion
    is strong and weak and return two objects - in the first
    against whom the champion is stronger(string 5 element), in the second
    against whom the champion  is weaker(string 5 element)"""
    champions_names = data.find_all('i', 'img-wrap border-2', limit=10)

    strong = ''
    weak = ''
    x = 0

    for champ in champions_names:
        name = champ.find('img', alt=True)['alt'] + '\n'
        name = name.split(' ')
        if x < 5:
            strong += name[0] + ', '
        else:
            weak += name[0] + ', '
        x += 1

    return strong[:-2], weak[:-2]


@base_exception
def get_champion_runes(data):
    """Get runes for champion. First runes(4) - core runes, 
    second runes - extra runes(2). Return two objects in 
    string type"""
    class_runes = data.find('div', class_='rune-block rune-block--new')
    runes = class_runes.find_all('span', limit=8)
    core_runes = ''
    extra_runes = ''
    
    x = 1
    for i in runes:
        if x == 1:
            core_runes += i.get_text() + ':\n'
        elif x < 6:
            core_runes += i.get_text() + ', '
        elif x == 6:
            extra_runes += i.get_text() + ':\n'
        else:
            extra_runes += i.get_text() + ', '
        x += 1
    
    return core_runes[:-2], extra_runes[:-2]


@base_exception
def get_all_information(champion):
    """Request and get all info about champion"""
    request = request_champion_info(champion)
    champion_info = get_champion_info(request)

    return champion_info
