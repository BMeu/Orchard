# -*- coding: utf-8 -*-

"""
    This module determines the base directory of |projectname|.

    .. attribute:: basedir
       :annotation: = /absolute/path/to/orchard

       .. admonition:: Example

          If |projectname| is installed at ``/opt/orchard``, ``basedir`` will automatically be
          set to ``/opt``.
"""

import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
