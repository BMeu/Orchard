# -*- coding: utf-8 -*-

"""
    Property Test: orchard.system_status.formatters.data
"""

import unittest

import hypothesis
import hypothesis.strategies as st

import orchard
import orchard.system_status.formatters.os as formatter


class OSPropertyTest(unittest.TestCase):

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

    @hypothesis.given(logins = st.integers())
    def test_current_logins(self, logins):
        formatted_value = formatter.current_logins(logins)
        if logins == 1:
            self.assertTrue('one' in formatted_value)
            self.assertFalse(str(logins) in formatted_value)
        else:
            self.assertFalse('one' in formatted_value)
            self.assertTrue(str(logins) in formatted_value)
