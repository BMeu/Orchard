# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.system.memory
"""

import collections
import unittest

import mock

import orchard
import orchard.system_status.system.memory as memory


class MemoryUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

        svmem = collections.namedtuple('svmem', ['available', 'total', 'used'])
        sswap = collections.namedtuple('sswap', ['free', 'total', 'used'])
        self.memory_usage = svmem(total = 4, available = 3, used = 1)
        self.swap_usage = sswap(total = 4, free = 3, used = 1)

    def tearDown(self):
        self.app_context.pop()

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_available(self, mock_psutil):
        mock_psutil.virtual_memory.return_value = self.memory_usage

        available = memory.available()
        self.assertTrue(mock_psutil.virtual_memory.called)
        self.assertEqual(available, 3)

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_total(self, mock_psutil):
        mock_psutil.virtual_memory.return_value = self.memory_usage

        total = memory.total()
        self.assertTrue(mock_psutil.virtual_memory.called)
        self.assertEqual(total, 4)

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_used(self, mock_psutil):
        mock_psutil.virtual_memory.return_value = self.memory_usage

        used = memory.used()
        self.assertTrue(mock_psutil.virtual_memory.called)
        self.assertEqual(used, 1)

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_swap_available(self, mock_psutil):
        mock_psutil.swap_memory.return_value = self.swap_usage

        available = memory.swap_available()
        self.assertTrue(mock_psutil.swap_memory.called)
        self.assertEqual(available, 3)

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_swap_total(self, mock_psutil):
        mock_psutil.swap_memory.return_value = self.swap_usage

        total = memory.swap_total()
        self.assertTrue(mock_psutil.swap_memory.called)
        self.assertEqual(total, 4)

    @mock.patch('orchard.system_status.system.memory.psutil')
    def test_swap_used(self, mock_psutil):
        mock_psutil.swap_memory.return_value = self.swap_usage

        used = memory.swap_used()
        self.assertTrue(mock_psutil.swap_memory.called)
        self.assertEqual(used, 1)
