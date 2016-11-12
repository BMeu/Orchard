# -*- coding: utf-8 -*-

"""
    Formatter functions for temperatures.
"""

import flask_babel


def celsius(value: float) -> str:
    """
        Format a temperature with °C as unit.

        :param value: The temperature in °C.
        :return: The temperature with °C as unit.
    """

    return '{value}°C'.format(value = flask_babel.format_decimal(value, format = '#,##0.0'))


def celsius_to_fahrenheit(value: float) -> str:
    """
        Convert and format a temperature given in °C to °F.

        :param value: The temperature in °C.
        :return: The temperature converted to °F and formatted with the correct unit.
    """
    fahrenheit = (value * 1.8) + 32
    return '{value}°F'.format(value = flask_babel.format_decimal(fahrenheit, format = '#,##0.0'))
