# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.system.os
"""

import datetime
import subprocess
import time
import unittest

import mock
import psutil

import orchard
import orchard.system_status.system.os as os


class OSUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    @mock.patch('orchard.system_status.system.os.psutil')
    def test_boot_time(self, mock_psutil):
        boot_datetime = datetime.datetime(1992, 2, 5, 0, 0, 0, 0)
        mock_psutil.boot_time.return_value = time.mktime(boot_datetime.timetuple())

        boot_time = os.boot_time()
        self.assertTrue(mock_psutil.boot_time.called)
        self.assertEqual(boot_time, boot_datetime)

    @mock.patch('orchard.system_status.system.os.psutil')
    def test_current_logins(self, mock_psutil):
        mock_psutil.users.return_value = [
            psutil._common.suser(name = 'orchard', terminal='tty1', host = 'localhost',
                                 started = 697248000.0),
            psutil._common.suser(name = 'orchard', terminal='tty2', host = 'localhost',
                                 started = 697251600.0)
        ]

        current_logins = os.current_logins()
        self.assertTrue(mock_psutil.users.called)
        self.assertEqual(current_logins, 2)

    @mock.patch('orchard.system_status.system.os.datetime')
    def test_current_time(self, mock_datetime):
        os.current_time()
        self.assertTrue(mock_datetime.datetime.now.called)

    @mock.patch('subprocess.Popen')
    def test_gpu_version(self, mock_popen):
        data = (b'Oct 25 2016 16:03:42\n' +
                b'Copyright (c) 2012 Broadcom\n' +
                b'version f74adfcae00b721627eab44590728c13860bcbc2 (clean) (release))')
        expected_value = os.gpu(hash = 'f74adfcae00b721627eab44590728c13860bcbc2',
                                compile_time = datetime.datetime(2016, 10, 25, 16, 3, 42))
        mock_process = mock.Mock()
        attributes = {
            'communicate.return_value': (data, '')
        }
        mock_process.configure_mock(**attributes)
        mock_popen.return_value = mock_process

        gpu_firmware = os.gpu_version()
        mock_popen.assert_called_with(['sudo', 'vcgencmd', 'version'], stdout = subprocess.PIPE)
        self.assertEqual(gpu_firmware, expected_value)

    @mock.patch('subprocess.Popen')
    def test_kernel_version(self, mock_popen):
        data = b'Linux raspberry 4.4.30-v7+ #919 SMP Tue Nov 1 16:57:28 GMT 2016 armv7l'
        expected_value = os.kernel(system = 'Linux raspberry', version = '4.4.30-v7+ #919',
                                   compile_time = datetime.datetime(2016, 11, 1, 16, 57, 28))
        mock_process = mock.Mock()
        attributes = {
            'communicate.return_value': (data, '')
        }
        mock_process.configure_mock(**attributes)
        mock_popen.return_value = mock_process

        kernel_version = os.kernel_version()
        mock_popen.assert_called_with(['uname', '-snvrm'], stdout = subprocess.PIPE)
        self.assertEqual(kernel_version, expected_value)

    @mock.patch('subprocess.Popen')
    def test_last_login(self, mock_popen):
        data = (b'reboot   system boot  4.4.21-v7+       Thu Jan  1 01:00:02 1970 - ' +
                b'Sat Nov  5 11:49:58 2016 (17110+10:49\n' +
                b'bastian  pts/0        192.168.0.1   Fri Nov  4 20:18:53 2016 - ' +
                b'down                      (00:00)\n' +
                b'bastian  pts/0        192.168.0.1   Fri Nov  4 20:16:24 2016 - ' +
                b'Fri Nov  4 20:17:21 2016  (00:00)\n')
        expected_value = os.login(user = 'bastian', host = '192.168.0.1',
                                  login_time = datetime.datetime(2016, 11, 4, 20, 18, 53))
        mock_process = mock.Mock()
        attributes = {
            'communicate.return_value': (data, '')
        }
        mock_process.configure_mock(**attributes)
        mock_popen.return_value = mock_process

        login = os.last_login()
        mock_popen.assert_called_with(['last', '-F'], stdout = subprocess.PIPE)
        self.assertTupleEqual(login, expected_value)

        data = (b'reboot   system boot  4.4.21-v7+       Thu Jan  1 01:00:02 1970 - ' +
                b'Sat Nov  5 11:49:58 2016 (17110+10:49\n' +
                b'reboot   system boot  4.4.21-v7+       Thu Jan  1 01:00:02 1970 - ' +
                b'Sat Nov  5 11:49:59 2016 (17110+10:49\n')
        expected_value = os.login(user = 'user', host = 'host',
                                  login_time = datetime.datetime(1970, 1, 1, 0, 0, 0))
        mock_process = mock.Mock()
        attributes = {
            'communicate.return_value': (data, '')
        }
        mock_process.configure_mock(**attributes)
        mock_popen.return_value = mock_process

        login = os.last_login()
        mock_popen.assert_called_with(['last', '-F'], stdout = subprocess.PIPE)
        self.assertTupleEqual(login, expected_value)

    @mock.patch('orchard.system_status.system.os.boot_time')
    @mock.patch('orchard.system_status.system.os.datetime')
    def test_run_time(self, mock_datetime, mock_boot_time):
        mock_boot_time.return_value = datetime.datetime(1992, 2, 5, 0, 0, 0, 0)
        mock_datetime.datetime.now.return_value = datetime.datetime(1992, 2, 5, 1, 0, 0, 0)

        run_time = os.run_time()
        self.assertTrue(mock_boot_time.called)
        self.assertTrue(mock_datetime.datetime.now.called)
        self.assertEqual(run_time, datetime.timedelta(0, 3600))

    @mock.patch('orchard.system_status.system.os.psutil')
    def test_running_processes(self, mock_psutil):
        mock_psutil.pids.return_value = [0, 1, 1, 2, 3, 5, 8, 13]

        running_processes = os.running_processes()
        self.assertTrue(mock_psutil.pids.called)
        self.assertEqual(running_processes, 8)
