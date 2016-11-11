# -*- coding: utf-8 -*-

"""
    Formatter functions for data values (e.g. data volume).
"""


def bytes_to_human_readable(value: float) -> str:
    """
        Convert a value from Byte into a human readable format (using binary prefixes ``Ki``,
        ``Mi``, ...).

        :param value: The data volume in Bytes.
        :return: The value converted to the best prefix with one decimal place.
    """
    readable = '{value:.1f} {prefix}B'
    for prefix in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(value) < 1024.0:
            return readable.format(value = value, prefix = prefix)
        value /= 1024

    return readable.format(value = value, prefix = 'Yi')
