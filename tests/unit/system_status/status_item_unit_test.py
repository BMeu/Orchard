# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.status_item
"""

import datetime
import unittest

import orchard.system_status


class StatusItemUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_initialization(self):
        status_item = orchard.system_status.StatusItem('Item 1', str)
        self.assertEqual(status_item._label, 'Item 1')
        self.assertEqual(status_item._value_function, str)
        self.assertListEqual(status_item._function_args, [])

        status_item = orchard.system_status.StatusItem('Item 2', str, [42])
        self.assertEqual(status_item._label, 'Item 2')
        self.assertEqual(status_item._value_function, str)
        self.assertListEqual(status_item._function_args, [42])

        status_item = orchard.system_status.StatusItem('Item 3', str, {'object': 42})
        self.assertEqual(status_item._label, 'Item 3')
        self.assertEqual(status_item._value_function, str)
        self.assertDictEqual(status_item._function_args, {'object': 42})

    def test_label(self):
        status_item = orchard.system_status.StatusItem('Item 1', str)
        self.assertEqual(status_item.label, 'Item 1')

    def test_get_current_value(self):
        status_item = orchard.system_status.StatusItem('Item 1', str)
        self.assertEqual(status_item.get_current_value(), '')

        status_item = orchard.system_status.StatusItem('Item 2', str, [42])
        self.assertEqual(status_item.get_current_value(), '42')

        status_item = orchard.system_status.StatusItem('Item 3', str, {'object': 42})
        self.assertEqual(status_item.get_current_value(), '42')

        # The current value depends on the time and should not stay the same.
        status_item = orchard.system_status.StatusItem('Item 4', datetime.datetime.now)
        value_1 = status_item.get_current_value()
        value_2 = status_item.get_current_value()
        self.assertNotEqual(value_1, value_2)
