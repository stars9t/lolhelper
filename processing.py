def message_pretify(champion_info):
    message = (
    f'-----------------------------------\n'
    f"Name: {champion_info['name']}\n"
    f'-----------------------------------\n'
    f"Role: {champion_info['role']}\n"
    f'-----------------------------------\n'
    f'Core weapons:\n\n'
    f"{champion_info['base_weapons']}"
    f'-----------------------------------\n'
    f'Luxury weapons:\n\n'
    f"{champion_info['late_weapons']}"
    f'-----------------------------------\n'
    f'Champions is Strong Against:\n'
    f"{champion_info['strong_against']}\n"
    f'-----------------------------------\n'
    f'Champion is Weak Against:\n'
    f"{champion_info['weak_against']}\n"
    f'-----------------------------------\n'
    f'Champion runes:\n'
    f"{champion_info['core_runes']}\n"
    f"{champion_info['extra_runes']}\n"
    )
    return message