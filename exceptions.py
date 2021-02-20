import functools

from logs import logger


def base_exception(fn):
    """
    Standard decorator for except all exceptions and
    write error message in log.
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f'{fn.__module__}.py: {fn.__name__}: {e}')
    return inner
