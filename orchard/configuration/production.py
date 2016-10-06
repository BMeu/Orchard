# -*- coding: utf-8 -*-

"""
    Production mode configuration.
"""

from orchard.configuration import Default


class Production(Default):
    """
        Configuration values used in production mode.
    """

    DEBUG = False

    TESTING = False
