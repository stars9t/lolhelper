from requests import base_exception


@base_exception
def message_prettify(champion):
    """
    Beautiful formatting text.
    """
    message = (
    f'-----------------------------------\n'
    f"Name: {champion.name}\n"
    f'-----------------------------------\n'
    f'Role: {champion.roles}\n'
    f'-----------------------------------\n'
    f'Core weapons:\n\n'
    f"{champion.core_weapons}\n"
    f'-----------------------------------\n'
    f'Luxury weapons:\n\n'
    f'{champion.late_weapons}\n'
    f'-----------------------------------\n'
    f'Champions is Strong Against:\n\n'
    f'{champion.strong_against}\n'
    f'-----------------------------------\n'
    f'Champion is Weak Against:\n\n'
    f'{champion.weak_against}\n'
    f'-----------------------------------\n'
    f'Champion runes:\n'
    f'{champion.core_runes}\n'
    f'{champion.extra_runes}\n'
    )
    return message


def items_to_text(items: list) -> str:
    """
    Converting more items to text for
    easy use in prettify.
    """
    output = ''
    for item in items:
        output += item + ', '
    
    return output[:-2]


def runes_to_text(runes: dict) -> str:
    """
    Converting runes to text for
    easy use in prettify.
    """
    output = f'{runes["branch_name"]}:\n\n'

    for rune in runes['runes']:
        output += rune + ', '

    return output[:-2] + '\n'
    
