# -*- coding: utf-8 -*-

"""
    Retrieve information on the network.
"""

import enum
from typing import Dict
import socket

import ipgetter2
import psutil

import orchard.extensions


class IPVersion(enum.Enum):
    """
        Versions of the Internet Protocol.
    """
    v4 = 4
    v6 = 6


@orchard.extensions.cache.memoize()
def hostname() -> str:
    """
        Get the host name of the system.

        :return: The host name.
    """
    return socket.gethostname()


@orchard.extensions.cache.memoize()
def external_ip_address() -> str:
    """
        Get the IP address of the system as seen from outside the local network.

        :return: The IP address
    """
    ipgetter = ipgetter2.IPGetter()
    addresses = ipgetter.get()
    return str(addresses.v6) if str(addresses.v6) != '::' else str(addresses.v4)


def ip_address(interface: str, ip_version: IPVersion) -> str:
    """
        Get the IP address in the given IP version for the specified interface.

        :param interface: The interface for which the IP address will be returned.
        :param ip_version: The version of the Internet Protocol.
        :return: The associated IP address. If the interface does not exist, or if the specified
                 interface does not have an address in the given IP version, return an empty string.
    """
    all_adresses = ip_addresses()
    interface_addresses = all_adresses.get(interface, {})
    return interface_addresses.get(ip_version, '')


def ip_addresses() -> Dict[str, Dict[IPVersion, str]]:
    """
        Get the IPv4 and IPv6 addresses of all network interfaces (except the loopback interface).

        :return: The outer dictionary's key is the name of the network interface, the corresponding
                 value is a dictionary with possibly two entries: one with key ``IPVersion.v4``
                 for the IPv4 address of the interface, the other with key ``'IPVersion.v6'`` for
                 the IPv6 address of the interface.
    """
    unfiltered_addresses = psutil.net_if_addrs()
    filtered_addresses = {}
    for interface, addresses in unfiltered_addresses.items():
        # Ignore the loopback interface.
        if interface == 'lo':
            continue

        filtered_addresses[interface] = {}
        for address in addresses:
            # Add IPv4 and IPv6 addresses to the output.
            if address.family == socket.AF_INET:
                filtered_addresses[interface][IPVersion.v4] = address.address
            elif address.family == socket.AF_INET6:
                filtered_addresses[interface][IPVersion.v6] = address.address

    return filtered_addresses
