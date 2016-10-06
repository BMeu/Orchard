# -*- coding: utf-8 -*-

"""
    Default configuration.
"""

import os

from orchard.configuration import basedir


class Default:
    """
        Default configuration values that are valid for all operation modes.
    """

    # Paths.
    BUILD_PATH = os.path.join(basedir, 'build')
    INSTANCE_PATH = os.path.join(basedir, 'instance')
    LOG_PATH = os.path.join(INSTANCE_PATH, 'log')

    # Project name.
    PROJECT_NAME = 'Orchard'
