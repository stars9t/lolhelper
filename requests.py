from bs4 import BeautifulSoup
import urllib3 
import config 
from logs import logger
import functools


http = urllib3.PoolManager()
soup = BeautifulSoup()

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
        f'https://www.leagueofgraphs.com/ru/champions/builds/{champion}', 
        None, 
        config.headers
    )

    return request


@base_exception
def get_champion_info(request):
    """Get all info about champion in text format"""
    request_data = BeautifulSoup(request.data, 'lxml')

    all_information = {
        'name': get_request_data_text(request_data, 'h2'),
        'role': get_request_data_text(request_data,
        'div', 'bannerSubtitle'),
        'base_weapons': get_base_weapons(request_data),
        'late_weapons': get_late_weapons(request_data)
    }
    return all_information


@base_exception
def get_request_data_text(soup, element, class_css = None):
    """Subsidiary function for get text from html code"""
    if class_css == None:
        return soup.find(element).get_text().strip()
    else:
        return soup.find(element, class_=class_css).get_text().strip()
     

@base_exception
def get_base_weapons(soup):
    """Get text about all base weapons for champion"""
    request_data = soup.find('div', class_='medium-13')
    base_weapons = request_data.find_all('img', alt=True)
    base_weapons_text = ""
    for img in base_weapons:
        base_weapons_text += img['alt'] + '\n'

    return base_weapons_text


@base_exception
def get_late_weapons(soup):
    """Get text about all late weapons for champion"""
    request_data = soup.find('div', class_='medium-13')
    next_request_data = request_data.find_next(class_='medium-13')
    late_weapons = next_request_data.find_all('img', alt=True)
    late_weapons_text = ""
    for img in late_weapons:
        late_weapons_text += img['alt'] + '\n'
    
    return late_weapons_text


@base_exception
def get_all_information(champion):
    """Request and get all info about champion"""
    request = request_champion_info(champion)
    champion_info = get_champion_info(request)
    return champion_info
