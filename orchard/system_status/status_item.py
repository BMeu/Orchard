# -*- coding: utf-8 -*-

"""
    This module provides the ``StatusItem`` class used for single system system information.
"""

from typing import Any, Callable, Dict, List, Union


class StatusItem:
    """
        A status item collects information on
    """

    def __init__(self, label: str, value_function: Callable,
                 function_args: Union[Dict[str, Any], List[Any]] = None):
        """
            :param label: A description for this item.
            :param value_function: The function used to retrieve the actual value of the status
                                   item.
            :param function_args: A list (for unnamed arguments) or a dictionary (for named
                                  arguments) of arguments that will be passed to the
                                  ``value_function``.
        """
        self._label = label
        self._value_function = value_function

        if function_args is not None:
            self._function_args = function_args
        else:
            self._function_args = []

    @property
    def label(self) -> str:
        """
            Get a description of the status item.

            :return: A description of this item.
        """
        return self._label

    def get_current_value(self) -> str:
        """
            Get the actual value of the status item.

            :return: The current value of ``value_function`` with applied ``function_args``,
                     cast to a string.
        """
        if isinstance(self._function_args, dict):
            # noinspection PyCallingNonCallable
            value = self._value_function(**self._function_args)
        else:
            # noinspection PyCallingNonCallable
            value = self._value_function(*self._function_args)

        return str(value)
