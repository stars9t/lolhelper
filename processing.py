def message_pretify(champion_info):
    message = f"""
    ----={champion_info['name']}=----
    \nРоль: {champion_info['role']}
    \n--= Основное оружие=--
    \n{champion_info['base_weapons']}
    \n--= Позднее оружие=--
    \n{champion_info['late_weapons']}
    """
    return message