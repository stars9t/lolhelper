from loguru import logger


logger.add('logs.log',
            format='{time} {message}',
            level='INFO', rotation='5 MB',
            compression='zip')


