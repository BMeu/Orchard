# -*- coding: utf-8 -*-

"""
    Retrieve information on system memory (RAM).
"""

import psutil


def free() -> int:
    """
        Get the amount of memory available for usage.

        :return: The memory in Bytes that can be used.
    """
    memory = psutil.virtual_memory()
    return memory.free


def total() -> int:
    """
        Get the total amount of memory.

        :return: The total amount of memory in Bytes.
    """
    memory = psutil.virtual_memory()
    return memory.total


def used() -> int:
    """
        Get the amount of memory used.

        :return: The amount of memory in Bytes that is being used.
    """
    return total() - free()


def swap_available() -> int:
    """
        Get the amount of swap memory available for usage.

        :return: The amount of swap memory in Bytes that can be used.
    """
    swap = psutil.swap_memory()
    return swap.free


def swap_total() -> int:
    """
        Get the total amount of swap memory.

        :return: The total amount of swap memory in Bytes.
    """
    swap = psutil.swap_memory()
    return swap.total


def swap_used() -> int:
    """
        Get the amount of swap memory used.

        :return: The amount of swap memory in Bytes that is being used.
    """
    swap = psutil.swap_memory()
    return swap.used
