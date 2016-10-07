# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.app
"""

import unittest

import orchard


class AppUnitTest(unittest.TestCase):

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
        self.assertTrue('Welcome to the Orchard!' in data)

        response = self.client.get('/BMeu')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Welcome to the Orchard, BMeu!' in data)
