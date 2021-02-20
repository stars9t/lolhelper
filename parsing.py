from bs4 import BeautifulSoup

from exceptions import base_exception


@base_exception
def parse_champion_name(data: BeautifulSoup) -> str:
    """
    Parse champion's name.
    """
    champion_info = data.find('div',
        class_='champ__header__left__main')
    champion_name = champion_info.find('h2').get_text()

    return champion_name


@base_exception
def parse_champion_role(data: BeautifulSoup) -> list:
    """
    Parse champion's role or roles if multiple.
    """
    champions_status = data.find('span', class_='stat-source')
    roles_stack = champions_status.find_all('span',
        class_='stat-source__btn', limit=3)

    roles = [role.get_text() for role in roles_stack]

    return roles


@base_exception
def parse_core_weapons(data: BeautifulSoup) -> list:
    """
    Parse core weapons for the champion.
    """
    core_items_stack = data.find('div', class_='item-block--crossover')
    core_items_img = core_items_stack.find_all('img', alt=True)

    core_items = [img['alt'] for img in core_items_img]

    return core_items
    
    
@base_exception
def parse_late_weapons(data: BeautifulSoup) -> list:
    """
    Parse late weapons for the champion.
    """
    late_items_stack = data.find_all('div',
        class_='item-block__top item-block__top--inline block-luxury')

    late_items = [i.find('img', alt=True)['alt'] for i in late_items_stack]


    return late_items


@base_exception
def parse_other_champions(data: BeautifulSoup, power: str) -> list:
    """
    Parse the names of champions who are stronger or weak.
    :param power: strong or weak.
    """
    if power == 'strong':
        champ_stack = data.find_all('i', 'img-wrap border-2', limit=5)
    elif power == 'weak':
        champ_stack = data.find_all('i', 'img-wrap border-2', limit=10)[5:]
    else:
        raise ValueError('branch not weak or strong')

    champ_stack_img = [i.find('img', alt=True)['alt'] for i in champ_stack]
    # in name stay: [name role percent]
    champions = [name.split(' ')[0] for name in champ_stack_img]

    return champions 


@base_exception
def parse_core_runes(data: BeautifulSoup) -> dict:
    """
    Parse core runes for the champion.
    First element in dict is name of branch for runes.
    Second element is list for runes.
    """
    found_runes = data.find('div', class_='rune-block rune-block--new')
    core_runes_stack = found_runes.find_all('span', limit=5)
    core_runes = {'branch_name': core_runes_stack[0].get_text()}

    runes = [rune.get_text() for rune in core_runes_stack]

    core_runes['runes'] = runes

    return core_runes 


@base_exception
def parse_extra_runes(data: BeautifulSoup) -> dict:
    """
    Parse extra runes for champion.
    First element in dict is name of branch for runes.
    Second element is list of runes.
    """
    all_runes = data.find('div', class_='rune-block rune-block--new')
    extra_runes_stack = all_runes.find_all('span', limit=8)[5:]
    extra_runes = {'branch_name': extra_runes_stack[0].get_text()}

    runes = [rune.get_text() for rune in extra_runes_stack[1:]]

    extra_runes['runes'] = runes
    
    return extra_runes
