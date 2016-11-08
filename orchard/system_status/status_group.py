# -*- coding: utf-8 -*-

"""
    This module provides the ``StatusGroup`` class collecting multiple :cls:`StatusItem`s.
"""

from typing import Iterator

from orchard.system_status import StatusItem


class StatusGroup:
    """
        A StatusGroup collects multiple :cls:`StatusItem`s under a specific header.
    """

    def __init__(self, label: str):
        """
            :param label: A header for the status group.
        """
        self._label = label
        self._items = []

    @property
    def label(self) -> str:
        """
            Get a description of the status group.

            :return: A description of this group.
        """
        return self._label

    def append(self, status_item: StatusItem):
        """
            Add a status item to the end of the group.

            :param status_item: The status item
        """
        self._items.append(status_item)

    def __iter__(self) -> Iterator:
        """
            Get an iterator over all added :cls:`StatusItem` objects, in the order they have been
            added.

            :return: An iterator over all status items.
        """
        return iter(self._items)
