# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.formatters.data
"""

import datetime
import unittest

import orchard
import orchard.system_status.formatters.os as formatter
import orchard.system_status.system.os as os


class OSUnitTest(unittest.TestCase):

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

    def test_current_logins(self):
        self.assertEqual(formatter.current_logins(0), 'Currently, 0 users are logged in.')
        self.assertEqual(formatter.current_logins(1), 'Currently, one user is logged in.')
        self.assertEqual(formatter.current_logins(2), 'Currently, 2 users are logged in.')

    def test_gpu(self):
        gpu_version = os.gpu(hash = 'f74adfcae00b721627eab44590728c13860bcbc2',
                             compile_time = datetime.datetime(1992, 2, 5, 0, 0, 0))
        self.assertEqual(formatter.gpu(gpu_version),
                         'f74adfcae00b721627eab44590728c13860bcbc2 of Feb 5, 1992, 12:00:00 AM')

    def test_kernel(self):
        kernel_version = os.kernel(system = 'Linux', version = '4.4.4',
                                   compile_time = datetime.datetime(1992, 2, 5, 0, 0, 0))
        self.assertEqual(formatter.kernel(kernel_version),
                         'Linux 4.4.4 of Feb 5, 1992, 12:00:00 AM')

    def test_login(self):
        login = os.login(user = 'bastian', host = 'localhost',
                         login_time = datetime.datetime(1992, 2, 5, 0, 0, 0))
        self.assertEqual(formatter.last_login(login),
                         'User "bastian" from localhost on Feb 5, 1992, 12:00:00 AM')
