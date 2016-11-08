# -*- coding: utf-8 -*-

"""
    This package includes the Flask blueprint and all related functionality for displaying system
    information.
"""

from .blueprint import blueprint

import orchard.system_status.views  # NOQA

__all__ = ['blueprint']
