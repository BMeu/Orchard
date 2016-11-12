# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.views.overview
"""

import unittest

import orchard


class OverviewUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="system-status-table"' in data)
