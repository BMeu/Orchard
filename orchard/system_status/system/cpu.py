# -*- coding: utf-8 -*-

"""
    Retrieve CPU information.
"""

import enum
import subprocess


class LoadPeriods(enum.Enum):
    """
        An enumeration of the periods of time for the CPU loads.
    """
    one = 0
    five = 1
    fifteen = 2


def load(load_period: LoadPeriods) -> float:
    """
        Get the load of the CPU over the given last period.

        :param load_period: The period of time for which the CPU load will be calculated.
        :return: The CPU load.
    """
    with open('/proc/loadavg', 'r') as load_file:
        line = load_file.read()

    loads = line.split(' ')
    try:
        load_value = loads[load_period.value]
    except IndexError:
        load_value = '0.0'

    return float(load_value)


def temperatue() -> float:
    """
        Get the current temperature of the CPU.

        .. attention::

            This function will only work on Raspbian!

        :return: The CPU temperature in degree Celsius.
    """
    process = subprocess.Popen(['sudo', 'vcgencmd', 'measure_temp'], stdout = subprocess.PIPE)
    output, _ = process.communicate()
    # noinspection PyTypeChecker
    return float(output[output.index(b'=') + 1:output.rindex(b'\'')])
