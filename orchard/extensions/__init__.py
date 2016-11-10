# -*- coding: utf-8 -*-

"""
    This module intializes (but does not configure) the Flask extensions.
"""

from .flask_babel import babel
from .flask_caching import cache

__all__ = ['babel', 'cache']
