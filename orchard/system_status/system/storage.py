# -*- coding: utf-8 -*-

"""
    Retrieve information on the usage of the storage (HDD, SSD, SD Card, ...).
"""

import psutil


def available() -> int:
    """
        The available amount of storage space.

        :return: The amount of storage space in Bytes.
    """
    storage = psutil.disk_usage('/')
    return storage.free


def total() -> int:
    """
        The total amount of space provided by the storage.

        :return: The amount of storage space in Bytes.
    """
    storage = psutil.disk_usage('/')
    return storage.total


def used() -> int:
    """
        The used amount of storage space.

        :return: The amount of storage space in Bytes.
    """
    storage = psutil.disk_usage('/')
    return storage.used
