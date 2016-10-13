# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.extensions.babel
"""

import unittest

import orchard
import orchard.extensions.flask_babel


class BabelUnitTest(unittest.TestCase):

    def setUp(self):
        self.app = orchard.create_app('Testing')
        self.app.config['LANGUAGES'] = {
            'de': 'Deutsch',
            'en': 'English'
        }

    def test_get_locale(self):
        # The preferred language is available.
        headers = {
            'Accept-Language': 'de,en;q=0.3'
        }
        with self.app.test_request_context('/', headers = headers):
            locale = orchard.extensions.flask_babel._get_locale()
            self.assertEqual(locale, 'de')

        # The preferred language is not available.
        headers = {
            'Accept-Language': 'fr,en;q=0.3'
        }
        with self.app.test_request_context('/', headers = headers):
            locale = orchard.extensions.flask_babel._get_locale()
            self.assertEqual(locale, 'en')

        # None of the accepted languages is available.
        headers = {
            'Accept-Language': 'fr,es;q=0.3'
        }
        with self.app.test_request_context('/', headers = headers):
            locale = orchard.extensions.flask_babel._get_locale()
            self.assertEqual(locale, 'en')
