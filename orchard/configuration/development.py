# -*- coding: utf-8 -*-

"""
    Development mode configuration.
"""

from orchard.configuration import Default


class Development(Default):
    """
        Configuration values used in development mode.
    """

    DEBUG = True

    TESTING = False
