# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.errors.e403
"""

import unittest

import orchard


class Error403UnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        app.config['BABEL_DEFAULT_LOCALE'] = 'en'
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/error403')
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        message = 'You do not currently have the correct permissions to view this page (code 403).'
        self.assertTrue(message in data)
