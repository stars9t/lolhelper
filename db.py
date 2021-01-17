import sqlite3
from logs import logger
from requests import base_exception


conn = sqlite3.connect('database.db')
c = conn.cursor()

def get_translated_name(rus_name):
    '''Translate ru name champion to english for searching champion in
    website with http request'''
    try:
        eng_name = c.execute(
        "SELECT eng FROM translate WHERE rus = '%s'" % rus_name
        )
        return eng_name.fetchone()[0]
    except TypeError:
        msg = f'{__name__}.py: {rus_name}: отсутсвует в базе данных'
        logger.info(msg)
        return None
    except Exception as e:
        logger.warning(f'{__name__}.py: {e}')
        return None
    

if __name__ == '__main__':
    c = conn.cursor()
    c.execute('''CREATE TABLE translate
                 ("id" integer,"rus" text, "eng" text,
                  PRIMARY KEY("ID" AUTOINCREMENT))''')