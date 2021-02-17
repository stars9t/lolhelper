import os


# Api telegram token for aiogram.
API_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Headers for request to website.
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/87.0.4280.141 Safari/537.36'}

# Link to database (dir or ip)
DATABASE = 'database.db'
