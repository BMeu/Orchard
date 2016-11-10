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

        .. attribute:: CACHE_DIR
           :annotation: = /path/to/your/cache/directory

           Used for the cache. By default within the :attr:`.INSTANCE_PATH`.

           :type: basestring

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

    # Available translations.
    LANGUAGES = {
        'de': 'Deutsch',
        'en': 'English'
    }
    """
        A dictionary of language codes with their respective name that are available in
        |projectname|.

        :type: Dict[str, str]
    """

    # Paths.
    BUILD_PATH = os.path.join(basedir, 'build')
    INSTANCE_PATH = os.path.join(basedir, 'instance')
    HYPOTHESIS_PATH = os.path.join(INSTANCE_PATH, 'hypothesis')
    LOG_PATH = os.path.join(INSTANCE_PATH, 'log')

    # Cache.
    CACHE_TYPE = 'filesystem'
    """
        The type of cache to use.

        :type: basestring
    """

    CACHE_DEFAULT_TIMEOUT = 60 * 60  # 1h
    """
        The time in seconds, objects will be stored in the cache.

        :type: int
    """

    CACHE_DIR = os.path.join(INSTANCE_PATH, 'cache')

    CACHE_THRESHOLD = 10
    """
        The maximum number of objects stored within the cache.

        :type: int
    """

    # Project name.
    PROJECT_NAME = 'Orchard'
    """
        The name of the application.

        :type: str
    """
