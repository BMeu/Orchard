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
    """
        Explicitly disable the debug mode.

        :type: bool
    """

    TESTING = False
    """
        Explicitly disable the testing mode.

        :type: bool
    """
