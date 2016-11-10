# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.system.cpu
"""

import subprocess
import unittest

import mock

import orchard
import orchard.system_status.system.cpu as cpu


class CPUUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

    def tearDown(self):
        self.app_context.pop()

    def test_load(self):
        patch = 'orchard.system_status.system.cpu.open'
        mock_file = mock.mock_open(read_data = '0.01 0.05 0.15 1/601 12343')
        with mock.patch(patch, mock_file, create = True) as mock_open:
            load_one = cpu.load(cpu.LoadPeriods.one)
            load_five = cpu.load(cpu.LoadPeriods.five)
            load_fifteen = cpu.load(cpu.LoadPeriods.fifteen)

        self.assertEqual(load_one, 0.01)
        self.assertEqual(load_five, 0.05)
        self.assertEqual(load_fifteen, 0.15)
        mock_open.assert_called_with('/proc/loadavg', 'r')

        mock_file = mock.mock_open(read_data = '0.01')
        with mock.patch(patch, mock_file, create = True) as mock_open:
            load_one = cpu.load(cpu.LoadPeriods.one)
            load_five = cpu.load(cpu.LoadPeriods.five)
            load_fifteen = cpu.load(cpu.LoadPeriods.fifteen)

        self.assertEqual(load_one, 0.01)
        self.assertEqual(load_five, 0.0)
        self.assertEqual(load_fifteen, 0.0)
        mock_open.assert_called_with('/proc/loadavg', 'r')

    @mock.patch('subprocess.Popen')
    def test_temperature(self, mock_popen):
        mock_process = mock.Mock()
        attributes = {
            'communicate.return_value': (b'temp=42.1337\'C', '')
        }
        mock_process.configure_mock(**attributes)
        mock_popen.return_value = mock_process
        temperature = cpu.temperatue()
        mock_popen.assert_called_with(['sudo', 'vcgencmd', 'measure_temp'],
                                      stdout = subprocess.PIPE)
        self.assertEqual(temperature, 42.1337)
