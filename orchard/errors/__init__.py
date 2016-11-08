# -*- coding: utf-8 -*-

"""
    Blueprint for handling all error pages.
"""

from .blueprint import blueprint
from .e400 import Error400View
from .e403 import Error403View
from .e404 import Error404View
from .e500 import Error500View

__all__ = ['blueprint', 'Error400View', 'Error403View', 'Error404View', 'Error500View']
