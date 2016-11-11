# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.formatters.data
"""

import datetime
import unittest

import orchard
import orchard.system_status.formatters.datetime as formatter


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

    def test_date_and_time(self):
        date_and_time = datetime.datetime(1992, 2, 5, 0, 0, 0)
        self.assertEqual(formatter.date_and_time(date_and_time), 'Feb 5, 1992, 12:00:00 AM')
