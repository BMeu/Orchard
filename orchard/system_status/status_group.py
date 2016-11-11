# -*- coding: utf-8 -*-

"""
    This module provides the ``StatusGroup`` class collecting multiple :cls:`StatusItem`s.
"""

from typing import Iterator, Union

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
        self._has_subgroups = False
        self._is_subgroup = False

    @property
    def label(self) -> str:
        """
            Get a description of the status group.

            :return: A description of this group.
        """
        return self._label

    def append(self, status: Union['StatusGroup', StatusItem]) -> bool:
        """
            Append either a StatusItem to the end of the group, or a StatusGroup. A StatusGroup
            will only be appended if ``self`` is not a subgroup itself and ``status`` does not
            have any subgroups (i.e. only one level of nesting is allowed).

            :param status: The status item or group.
            :return: True if the status has successfully been appended.
        """
        # Only allow one level of nesting.
        if isinstance(status, StatusGroup):
            if status._has_subgroups or self._is_subgroup:
                return False

            self._has_subgroups = True
            status._is_subgroup = True

        self._items.append(status)
        return True

    def __iter__(self) -> Iterator:
        """
            Get an iterator over all added :cls:`StatusItem` objects, in the order they have been
            added.

            :return: An iterator over all status items.
        """
        return iter(self._items)
