import functools

from logs import logger


def base_exception(fn):
    """
    Standart decorator for except all exceptions and 
    write error message in log.
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f'Ошибка парсинга, {__name__}: {e}')
    return inner