# -*- coding: utf-8 -*-

"""
    A collection of default configurations for certain operation modes of |projectname|.
"""

from .basedir import basedir
from .default import Default
from .development import Development
from .production import Production
from .testing import Testing

__all__ = ['basedir', 'Default', 'Development', 'Production', 'Testing']
