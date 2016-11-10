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

    CACHE_TYPE = 'null'
    """
        Disable caching during testing.

        :type: basestring
    """

    CACHE_NO_NULL_WARNING = True
    """
        Do not warn about disabled caching.

        :type: bool
    """
