# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.system.storage
"""

import unittest

import mock
import psutil

import orchard
import orchard.system_status.system.storage as storage


class StorageUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)
        self.disk_usage = psutil._common.sdiskusage(total = 4, used = 3, free = 1, percent = 1 / 4)

    def tearDown(self):
        self.app_context.pop()

    @mock.patch('orchard.system_status.system.storage.psutil')
    def test_available(self, mock_psutil):
        mock_psutil.disk_usage.return_value = self.disk_usage

        available = storage.available()
        mock_psutil.disk_usage.assert_called_with('/')
        self.assertEqual(available, 1)

    @mock.patch('orchard.system_status.system.storage.psutil')
    def test_total(self, mock_psutil):
        mock_psutil.disk_usage.return_value = self.disk_usage

        total = storage.total()
        mock_psutil.disk_usage.assert_called_with('/')
        self.assertEqual(total, 4)

    @mock.patch('orchard.system_status.system.storage.psutil')
    def test_used(self, mock_psutil):
        mock_psutil.disk_usage.return_value = self.disk_usage

        used = storage.used()
        mock_psutil.disk_usage.assert_called_with('/')
        self.assertEqual(used, 3)
