# -*- coding: utf-8 -*-

"""
    Property Test: orchard.system_status.status_group
"""

import hypothesis
import hypothesis.strategies as st
import unittest

import orchard.system_status


class StatusItemPropertyTest(unittest.TestCase):
    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    @hypothesis.given(label = st.text())
    def test_label(self, label):
        status_group = orchard.system_status.StatusGroup(label)
        self.assertEqual(status_group.label, label)
