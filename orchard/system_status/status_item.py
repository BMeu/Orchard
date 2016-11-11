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
                 function_args: Union[Dict[str, Any], List[Any]] = None,
                 formatter: Union[str, Callable[[Any], str]] = None):
        """
            :param label: A description for this item.
            :param value_function: The function used to retrieve the actual value of the status
                                   item.
            :param function_args: A list (for unnamed arguments) or a dictionary (for named
                                  arguments) of arguments that will be passed to the
                                  ``value_function``.
            :param formatter: If this is a function, ``function_args``'s return value will
                              directly be passed to the function for formatting; the expected
                              return type is ``str``. If ``formatter`` is a string,
                              it is expected to contain the format parameter ``{value}`` which
                              will be replaced with the actual raw value using ``str.format()``. If
                              ``None`` is given, the value will simply be formatted using ``str()``.
        """
        self._label = label
        self._value_function = value_function

        if function_args is not None:
            self._function_args = function_args
        else:
            self._function_args = []

        self._formatter = formatter

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
                     formatted using ``formatter`` (if given).
        """
        if isinstance(self._function_args, dict):
            # noinspection PyCallingNonCallable
            value = self._value_function(**self._function_args)
        else:
            # noinspection PyCallingNonCallable
            value = self._value_function(*self._function_args)

        if callable(self._formatter):
            formatted_value = self._formatter(value)
        elif isinstance(self._formatter, str):
            formatted_value = self._formatter.format(value = value)
        else:
            formatted_value = str(value)

        return formatted_value
