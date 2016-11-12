# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.formatters.data
"""

import unittest

import orchard
import orchard.system_status.formatters.data as formatter


class DataUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.request_context = app.test_request_context()
        self.request_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_bytes_to_human_readable(self):

        readable = formatter.bytes_to_human_readable(-1025)
        self.assertEqual(readable, '-1.0 KiB')

        readable = formatter.bytes_to_human_readable(-42)
        self.assertEqual(readable, '-42.0 B')

        readable = formatter.bytes_to_human_readable(42)
        self.assertEqual(readable, '42.0 B')

        readable = formatter.bytes_to_human_readable(42 * 1024)
        self.assertEqual(readable, '42.0 KiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024)
        self.assertEqual(readable, '42.0 MiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024)
        self.assertEqual(readable, '42.0 GiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(readable, '42.0 TiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(readable, '42.0 PiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(readable, '42.0 EiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 *
                                                     1024)
        self.assertEqual(readable, '42.0 ZiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 *
                                                     1024 * 1024)
        self.assertEqual(readable, '42.0 YiB')

        readable = formatter.bytes_to_human_readable(42 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 *
                                                     1024 * 1024 * 1024)
        self.assertEqual(readable, '43,008.0 YiB')
