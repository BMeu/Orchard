# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.errors.e500
"""

import unittest

import orchard


class Error500UnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/error500')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        message = ('The server encountered an internal error (code 500) ' +
                   'while processing your request.')
        self.assertTrue(message in data)
