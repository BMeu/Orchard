# -*- coding: utf-8 -*-

"""
    Instance configuration, possibly overwriting default values.
"""


class Configuration:
    """
        Instance specific configurations for |projectname| that should not be shared with anyone
        else (e.g. because of passwords).

        You can overwrite any of the values from :mod:`orchard.configuration` in this class.
    """

    SECRET_KEY = ''
