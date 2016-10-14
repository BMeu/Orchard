# -*- coding: utf-8 -*-

"""
    Blueprint for handling all error pages.
"""

from .blueprint import blueprint
from .e404 import Error404View
from .e500 import Error500View

__all__ = ['blueprint', 'Error404View', 'Error500View']
