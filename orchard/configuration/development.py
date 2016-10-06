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
    """
        Enable the debug mode.

        :type: bool
    """

    TESTING = False
    """
        Explicitly disable the testing mode.

        :type: bool
    """
