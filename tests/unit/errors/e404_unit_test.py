# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.errors.e404
"""

import unittest

import orchard


class Error404UnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/error404')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('The page you requested could not be found (code 404).' in data)
