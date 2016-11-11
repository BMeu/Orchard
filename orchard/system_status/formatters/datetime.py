# -*- coding: utf-8 -*-

"""
    Formatter functions for date and time values.
"""

import datetime

import flask_babel


def date_and_time(value: datetime.datetime) -> str:
    """
        Get a meaningful text with the given date and time.

        :param value: The date and time.
        :return: A meaningful text for the date and time.
    """
    return flask_babel.gettext('%(datetime)s', datetime = flask_babel.format_datetime(value))
