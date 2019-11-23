# -*- coding: utf-8 -*-

"""
    Unit Test: orchard.system_status.system.network
"""

import collections
import socket
import unittest

import mock
import psutil

import orchard
import orchard.system_status.system.network as network


class NetworkUnitTest(unittest.TestCase):

    def setUp(self):
        app = orchard.create_app('Testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies = True)

        self.addresses = {
            'eth0': {
                network.IPVersion.v4: '192.168.0.1',
                network.IPVersion.v6: '::1'
            },
            'wlan0': {
                network.IPVersion.v4: '192.168.0.2'
            }
        }

        self.interfaces = {
            'eth0': [
                psutil._common.snic(family = socket.AF_INET, address = '192.168.0.1',
                                    netmask = None, broadcast = None, ptp = None),
                psutil._common.snic(family = socket.AF_INET6, address = '::1',
                                    netmask = None, broadcast = None, ptp = None),
                psutil._common.snic(family = psutil.AF_LINK, address = 'c4:85:08:45:06:41',
                                    netmask = None, broadcast = None, ptp = None)
            ],
            'lo': [psutil._common.snic(family = socket.AF_INET, address = '127.0.0.1',
                                       netmask = None, broadcast = None, ptp = None)],
            'wlan0': [psutil._common.snic(family = socket.AF_INET, address = '192.168.0.2',
                                          netmask = None, broadcast = None, ptp = None)]
        }

    def tearDown(self):
        self.app_context.pop()

    @mock.patch('orchard.system_status.system.network.socket')
    def test_hostname(self, mock_socket):
        mock_socket.gethostname.return_value = 'TestSystem'

        hostname = network.hostname()
        self.assertTrue(mock_socket.gethostname.called)
        self.assertEqual(hostname, 'TestSystem')

    @mock.patch('orchard.system_status.system.network.ipgetter2.IPGetter.get')
    def test_external_ip_address_v4(self, mock_ipgetter):
        Address = collections.namedtuple('Address', 'v4 v6')
        mock_ipgetter.return_value = Address('3.141.59.26', '::')

        ip = network.external_ip_address()
        self.assertTrue(mock_ipgetter.called)
        self.assertEqual(ip, '3.141.59.26')

    @mock.patch('orchard.system_status.system.network.ipgetter2.IPGetter.get')
    def test_external_ip_address_v6(self, mock_ipgetter):
        Address = collections.namedtuple('Address', 'v4 v6')
        mock_ipgetter.return_value = Address('3.141.59.26', '2001:0db8:85a3:0000:0000:8a2e:0370:7334')

        ip = network.external_ip_address()
        self.assertTrue(mock_ipgetter.called)
        self.assertEqual(ip, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')

    @mock.patch('orchard.system_status.system.network.ip_addresses')
    def test_ip_address(self, mock_ip_addresses):
        mock_ip_addresses.return_value = self.addresses

        ip = network.ip_address('eth0', network.IPVersion.v4)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '192.168.0.1')

        ip = network.ip_address('eth0', network.IPVersion.v6)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '::1')

        ip = network.ip_address('wlan0', network.IPVersion.v4)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '192.168.0.2')

        ip = network.ip_address('wlan0', network.IPVersion.v6)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '')

        ip = network.ip_address('wlan1', network.IPVersion.v4)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '')

        ip = network.ip_address('wlan1', network.IPVersion.v6)
        self.assertTrue(mock_ip_addresses.called)
        self.assertEqual(ip, '')

    @mock.patch('orchard.system_status.system.network.psutil')
    def test_ip_addresses(self, mock_psutil):
        mock_psutil.net_if_addrs.return_value = self.interfaces

        ips = network.ip_addresses()
        self.assertTrue(mock_psutil.net_if_addrs.called)
        self.assertDictEqual(ips, self.addresses)
