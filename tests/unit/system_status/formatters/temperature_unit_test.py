# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.formatters.temperature
"""

import unittest

import flask_babel

import orchard
import orchard.system_status.formatters.temperature as formatter


class DataUnitTest(unittest.TestCase):

    def setUp(self):
        self.app = orchard.create_app('Testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()
        self.client = self.app.test_client(use_cookies = True)

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_celsius(self):
        self.assertEqual(formatter.celsius(42), '42.0°C')

        self.app.config['BABEL_DEFAULT_LOCALE'] = 'de'
        flask_babel.refresh()
        self.assertEqual(formatter.celsius(42), '42,0°C')

    def test_celsius_to_fahrenheit(self):
        self.assertEqual(formatter.celsius_to_fahrenheit(0), '32.0°F')
        self.assertEqual(formatter.celsius_to_fahrenheit(37), '98.6°F')
        self.assertEqual(formatter.celsius_to_fahrenheit(100), '212.0°F')

        self.app.config['BABEL_DEFAULT_LOCALE'] = 'de'
        flask_babel.refresh()
        self.assertEqual(formatter.celsius_to_fahrenheit(0), '32,0°F')
        self.assertEqual(formatter.celsius_to_fahrenheit(37), '98,6°F')
        self.assertEqual(formatter.celsius_to_fahrenheit(100), '212,0°F')
