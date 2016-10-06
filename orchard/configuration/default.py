# -*- coding: utf-8 -*-

"""
    Default configuration.
"""

import os

from orchard.configuration import basedir


class Default:
    """
        Default configuration values that are valid for all operation modes.

        .. attribute:: BUILD_PATH
           :annotation: = /path/to/your/build/directory

           Used for coverage reports and documentation builds.

           :type: str

        .. attribute:: HYPOTHESIS_PATH
           :annotation: = /path/to/your/hypothesis/directory

           Used by Hypothesis for saving examples of property tests. By default within the
           :attr:`.INSTANCE_PATH`.

           :type: str

        .. attribute:: INSTANCE_PATH
           :annotation: = /path/to/your/instance/directory

           Used for instance specific configurations.

           :type: str

        .. attribute:: LOG_PATH
           :annotation: = /path/to/your/log/directory

           Used for the logs by |projectname|. By default within the :attr:`.INSTANCE_PATH`.

           :type: basestring
    """

    # Paths.
    BUILD_PATH = os.path.join(basedir, 'build')
    INSTANCE_PATH = os.path.join(basedir, 'instance')
    HYPOTHESIS_PATH = os.path.join(INSTANCE_PATH, 'hypothesis')
    LOG_PATH = os.path.join(INSTANCE_PATH, 'log')

    # Project name.
    PROJECT_NAME = 'Orchard'
    """
        The name of the application.

        :type: str
    """
