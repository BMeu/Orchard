# -*- coding: utf-8 -*-

"""
    Testing configuration.
"""

from orchard.configuration import Default


class Testing(Default):
    """
        Configuration values used while testing |projectname|.
    """

    TESTING = True

    SERVER_NAME = 'localhost'
