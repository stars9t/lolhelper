import sqlite3
from typing import Optional

from logs import logger
from requests import base_exception


conn = sqlite3.connect('database.db')
c = conn.cursor()

def get_translated_name(name: str) -> Optional[str]:
    """Translate ru name champion to english for searching champion in
    website with http request"""
    try:
        translated_name = c.execute(
            "SELECT eng FROM translate WHERE rus = '%s'" % name
        )
        return translated_name.fetchone()[0]
    except TypeError:
        try:
            original_name = c.execute(
                'SELECT eng FROM translate WHERE eng = "%s"' % name
            )
            return original_name.fetchone()[0]
        except TypeError:
            msg = f'{__name__}.py: {name}: отсутсвует в базе данных'
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
