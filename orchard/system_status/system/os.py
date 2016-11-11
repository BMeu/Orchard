# -*- coding: utf-8 -*-

"""
    Retrieve information on the operating system.
"""

import collections
import datetime
import re
import subprocess

import psutil

import orchard.extensions

gpu = collections.namedtuple('gpu', ['hash', 'compile_time'])
kernel = collections.namedtuple('kernel', ['system', 'version', 'compile_time'])
login = collections.namedtuple('login', ['user', 'host', 'login_time'])


def boot_time() -> datetime.datetime:
    """
        Get the time the system was booted.

        :return: The date and time when the system booted.
    """
    return datetime.datetime.fromtimestamp(psutil.boot_time())


def current_logins() -> int:
    """
        Get the number of currently logged in users.

        :return: The number of users currently logged in to the system.
    """
    return len(psutil.users())


def current_time() -> datetime.datetime:
    """
        Get the current system time.

        :return: The time
    """
    return datetime.datetime.now()


@orchard.extensions.cache.memoize()
def gpu_version() -> gpu:
    """
        Get the firmware version of the GPU.

        .. attention::

            This function will only work on Raspbian!

        :return: The string identifying the current GPU firmware.
    """
    process = subprocess.Popen(['sudo', 'vcgencmd', 'version'], stdout = subprocess.PIPE)
    output, _ = process.communicate()

    # Simplify the output.
    gpu_details = output.decode('utf-8').replace('\n', ' ')
    gpu_details = re.sub(' +', ' ', gpu_details).split(' ')
    firmware_hash = gpu_details[9]

    year = gpu_details[2]
    month = gpu_details[0]
    day = gpu_details[1]
    time = gpu_details[3]
    compile_time = datetime.datetime.strptime('{month} {day} {year} {time}'.format(month = month,
                                                                                   day = day,
                                                                                   year = year,
                                                                                   time = time),
                                              '%b %d %Y %H:%M:%S')

    return gpu(hash = firmware_hash, compile_time = compile_time)


@orchard.extensions.cache.memoize()
def kernel_version() -> kernel:
    """
        Get information on the kernel version.

        :return: A named tuple :attr:`.kernel` with the system information, kernel version,
                 and kernel compile time.
    """
    process = subprocess.Popen(['uname', '-snvrm'], stdout = subprocess.PIPE)
    output, _ = process.communicate()

    # Simplify the output.
    kernel_details = output.decode('utf-8').split(' ')
    system = kernel_details[0] + ' ' + kernel_details[1]
    version = kernel_details[2] + ' ' + kernel_details[3]

    year = kernel_details[10]
    month = kernel_details[6]
    day = kernel_details[7]
    time = kernel_details[8]
    compile_time = datetime.datetime.strptime('{month} {day} {year} {time}'.format(month = month,
                                                                                   day = day,
                                                                                   year = year,
                                                                                   time = time),
                                              '%b %d %Y %H:%M:%S')

    return kernel(system = system, version = version, compile_time = compile_time)


def last_login() -> login:
    """
        Get information on the last login on the system.

        :return: A named tuple :attr:`.login` with the username, the host the user logged in
                 from, and the date and time of the last login.
    """
    process = subprocess.Popen(['last', '-F'], stdout = subprocess.PIPE)
    output, _ = process.communicate()

    # Create a default in case all lines contain 'reboot'.
    login_default = 'user 1 host 3 Jan 1 00:00:00 1970'

    # Simplify the output.
    lines = output.decode('utf-8').split('\n')
    login_details = ''
    for line in lines:  # pragma: no branch.
        if 'reboot' in line:
            continue

        login_details = line
        break

    if not login_details:
        login_details = login_default

    login_details = re.sub(' +', ' ', login_details).split(' ')

    user = login_details[0]
    host = login_details[2]

    year = login_details[7]
    month = login_details[4]
    day = login_details[5]
    time = login_details[6]
    login_time = datetime.datetime.strptime('{month} {day} {year} {time}'.format(month = month,
                                                                                 day = day,
                                                                                 year = year,
                                                                                 time = time),
                                            '%b %d %Y %H:%M:%S')

    return login(user = user, host = host, login_time = login_time)


def run_time() -> datetime.timedelta:
    """
        Get the time the system is up since the last boot.

        :return: The time difference between the call of this function and the boot time of the
                 system.
    """
    boot = boot_time()
    return datetime.datetime.now() - boot


def running_processes() -> int:
    """
        Get the number of running processes.

        :return: The number of all processes running on the system.
    """
    return len(psutil.pids())
