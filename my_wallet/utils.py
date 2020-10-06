import datetime


def now_timestamp() -> float:
    """
    Возвращает текущее время в формате UNIX-timestamp

    >>> isinstance(now_timestamp(), float)
    True
    """
    return datetime.datetime.now().timestamp()


# print(now_timestamp())