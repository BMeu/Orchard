# -*- coding: utf-8 -*-

"""
    Formatter functions for operating system related status information.
"""

import flask_babel

from orchard.system_status.system import os as os_info


def current_logins(value: int) -> str:
    """
        Get a meaningful sentence describing how many users are currently logged in.

        :param value: The number of currently logged in users.
        :return: The number of logged in users as a correct text.
    """
    return flask_babel.ngettext('Currently, one user is logged in.',
                                'Currently, %(num)d users are logged in.',
                                num = value)


def gpu(value: os_info.gpu) -> str:
    """
        Get a meaningful text describing the current GPU firmware.

        :param value: The information on the GPU firmware.
        :return: A meaningful text describing the GPU firmware.
    """
    return flask_babel.gettext('%(hash)s of %(compile_time)s',
                               hash = value.hash,
                               compile_time = flask_babel.format_datetime(value.compile_time))


def kernel(value: os_info.kernel) -> str:
    """
        Get a meaningful text describing the current kernel version.

        :param value: The information on the kernel version.
        :return: A meaningful text describing the kernel.
    """
    return flask_babel.gettext('%(system)s %(version)s of %(compile_time)s',
                               system = value.system, version = value.version,
                               compile_time = flask_babel.format_datetime(value.compile_time))


def last_login(value: os_info.login) -> str:
    """
        Get a meaningful text describing the last login.

        :param value: The information of the last login to the system.
        :return: A meaningful text describing the last login.
    """
    return flask_babel.gettext('User "%(user)s" from %(host)s on %(date)s',
                               user = value.user, host = value.host,
                               date = flask_babel.format_datetime(value.login_time))
