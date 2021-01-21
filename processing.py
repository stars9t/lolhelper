from typing import List, Dict

from requests import base_exception


@base_exception
def message_pretify(champion_info):
    roles = items_to_text(champion_info['roles'])
    core_w = items_to_text(champion_info['core_weapons'])
    late_w = items_to_text(champion_info['late_weapons'])
    strong_a = items_to_text(champion_info['strong_against'])
    weak_a = items_to_text(champion_info['weak_against'])
    c_runes = runes_to_text(champion_info['core_runes'])
    e_runes = runes_to_text(champion_info['extra_runes'])

    message = (
    f'-----------------------------------\n'
    f"Name: {champion_info['name']}\n"
    f'-----------------------------------\n'
    f'Role: {roles}\n'
    f'-----------------------------------\n'
    f'Core weapons:\n\n'
    f"{core_w}\n"
    f'-----------------------------------\n'
    f'Luxury weapons:\n\n'
    f'{late_w}\n'
    f'-----------------------------------\n'
    f'Champions is Strong Against:\n\n'
    f'{strong_a}\n'
    f'-----------------------------------\n'
    f'Champion is Weak Against:\n\n'
    f'{weak_a}\n'
    f'-----------------------------------\n'
    f'Champion runes:\n'
    f'{c_runes}\n'
    f'{e_runes}\n'
    )
    return message


def items_to_text(items: List) -> str:
    """Converting more items to text for easy use in prettify"""
    output = ''
    for item in items:
        output += item + ', '
    
    return output[:-2]


def runes_to_text(runes: Dict) -> str:
    """Converting runes to text for easy use in prettify"""
    output = f'{runes["branch_name"]}:\n\n'

    for rune in runes['runes']:
        output += rune + ', '

    return output[:-2] + '\n'
    
