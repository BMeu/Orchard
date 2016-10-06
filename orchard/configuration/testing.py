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
    """
        Ensable the testing mode.

        :type: bool
    """

    SERVER_NAME = 'localhost'
    """
        The name of the testing server.

        :type: str
    """
