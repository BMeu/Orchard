# -*- coding: utf-8 -*-

"""
    Unit Test: orchard
"""

import unittest

from orchard import app


class OrchardTest(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Welcome to the Orchard!' in data)
