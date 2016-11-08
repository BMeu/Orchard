# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.status_group
"""

import unittest

import orchard.system_status


class StatusGroupUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_initialization(self):
        status_group = orchard.system_status.StatusGroup('Group 1')
        self.assertEqual(status_group._label, 'Group 1')
        self.assertListEqual(status_group._items, [])

    def test_label(self):
        status_group = orchard.system_status.StatusGroup('Group 1')
        self.assertEqual(status_group.label, 'Group 1')

    def test_append(self):
        status_item_1 = orchard.system_status.StatusItem('Item 1', str)
        status_item_2 = orchard.system_status.StatusItem('Item 2', str)
        status_item_3 = orchard.system_status.StatusItem('Item 3', str)

        status_group = orchard.system_status.StatusGroup('Group 1')
        self.assertListEqual(status_group._items, [])

        status_group.append(status_item_2)
        self.assertListEqual(status_group._items, [status_item_2])

        status_group.append(status_item_3)
        self.assertListEqual(status_group._items, [status_item_2, status_item_3])

        status_group.append(status_item_1)
        self.assertListEqual(status_group._items, [status_item_2, status_item_3, status_item_1])

        status_group.append(status_item_3)
        self.assertListEqual(status_group._items, [status_item_2, status_item_3, status_item_1,
                                                   status_item_3])

    def test_iterator(self):
        status_item_1 = orchard.system_status.StatusItem('Item 1', str)
        status_item_2 = orchard.system_status.StatusItem('Item 2', str)
        status_item_3 = orchard.system_status.StatusItem('Item 3', str)
        status_group = orchard.system_status.StatusGroup('Group 1')

        items = []
        for status_item in status_group:
            items.append(status_item.label)
        self.assertEqual(items, [])

        status_group.append(status_item_2)
        status_group.append(status_item_3)
        status_group.append(status_item_1)
        status_group.append(status_item_3)
        items = []
        for status_item in status_group:
            items.append(status_item.label)
        self.assertEqual(items, ['Item 2', 'Item 3', 'Item 1', 'Item 3'])
