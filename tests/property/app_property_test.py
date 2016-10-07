# -*- coding: utf-8 -*-

"""
    Property Test: orchard.app
"""

import hypothesis
import hypothesis.strategies as st
import unittest

import orchard


class AppPropertyTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    @hypothesis.given(name = st.text(alphabet = ['a', 'b', 'c', 'A', 'B', 'C']))
    def test_index(self, name):
        response = self.client.get('/{name}'.format(name = name))
        data = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(name in data)
