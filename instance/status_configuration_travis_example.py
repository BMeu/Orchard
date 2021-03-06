# -*- coding: utf-8 -*-

"""
    Configuration of system status items and groups.
"""

import flask_babel

from orchard.system_status import StatusGroup, StatusItem
from orchard.system_status.formatters import data, datetime
from orchard.system_status.formatters import os as formatter_os
from orchard.system_status.system import cpu, memory, network, os, storage

# Create the status groups.
group_cpu = StatusGroup(flask_babel.lazy_gettext('CPU'))
group_cpu_load = StatusGroup(flask_babel.lazy_gettext('Load'))
group_memory = StatusGroup(flask_babel.lazy_gettext('Memory'))
group_memory_ram = StatusGroup(flask_babel.lazy_gettext('RAM'))
group_memory_swap = StatusGroup(flask_babel.lazy_gettext('Swap'))
group_network = StatusGroup(flask_babel.lazy_gettext('Network'))
group_network_internal_ip = StatusGroup(flask_babel.lazy_gettext('Internal IP'))
group_os = StatusGroup(flask_babel.lazy_gettext('Operating System'))
group_storage = StatusGroup(flask_babel.lazy_gettext('Storage'))
group_storage_usage = StatusGroup(flask_babel.lazy_gettext('Usage'))
group_users = StatusGroup(flask_babel.lazy_gettext('Users'))

# Operating System.
status_kernel = StatusItem(flask_babel.lazy_gettext('Kernel'), os.kernel_version,
                           formatter = formatter_os.kernel)
status_boottime = StatusItem(flask_babel.lazy_gettext('Boot Time'), os.boot_time,
                             formatter = datetime.date_and_time)
status_runtime = StatusItem(flask_babel.lazy_gettext('Runtime'), os.run_time,
                            formatter = flask_babel.format_timedelta)
status_current_time = StatusItem(flask_babel.lazy_gettext('Current Time'), os.current_time,
                                 formatter = datetime.date_and_time)
group_os.append(status_kernel)
group_os.append(status_boottime)
group_os.append(status_runtime)
group_os.append(status_current_time)

# Users.
status_current_logins = StatusItem(flask_babel.lazy_gettext('Current Logins'), os.current_logins,
                                   formatter = formatter_os.current_logins)
status_last_login = StatusItem(flask_babel.lazy_gettext('Last Login'), os.last_login,
                               formatter = formatter_os.last_login)
group_users.append(status_current_logins)
group_users.append(status_last_login)

# CPU.
status_processes = StatusItem(flask_babel.lazy_gettext('Running Processes'), os.running_processes)
status_load_one = StatusItem(flask_babel.lazy_gettext('1-Minute Average'), cpu.load,
                             [cpu.LoadPeriods.one], formatter = flask_babel.format_decimal)
status_load_five = StatusItem(flask_babel.lazy_gettext('5-Minute Average'), cpu.load,
                              [cpu.LoadPeriods.five], formatter = flask_babel.format_decimal)
status_load_fifteen = StatusItem(flask_babel.lazy_gettext('15-Minute Average'), cpu.load,
                                 [cpu.LoadPeriods.fifteen], formatter = flask_babel.format_decimal)
group_cpu.append(status_processes)
group_cpu.append(group_cpu_load)
group_cpu_load.append(status_load_one)
group_cpu_load.append(status_load_five)
group_cpu_load.append(status_load_fifteen)

# Storage.
status_storage_total = StatusItem(flask_babel.lazy_gettext('Total'), storage.total,
                                  formatter = data.bytes_to_human_readable)
status_storage_used = StatusItem(flask_babel.lazy_gettext('Used'), storage.used,
                                 formatter = data.bytes_to_human_readable)
status_storage_available = StatusItem(flask_babel.lazy_gettext('Available'), storage.available,
                                      formatter = data.bytes_to_human_readable)
group_storage.append(group_storage_usage)
group_storage_usage.append(status_storage_total)
group_storage_usage.append(status_storage_used)
group_storage_usage.append(status_storage_available)

# Memory.
status_mem_total = StatusItem(flask_babel.lazy_gettext('Total'), memory.total,
                              formatter = data.bytes_to_human_readable)
status_mem_used = StatusItem(flask_babel.lazy_gettext('Used'), memory.used,
                             formatter = data.bytes_to_human_readable)
status_mem_available = StatusItem(flask_babel.lazy_gettext('Free'), memory.free,
                                  formatter = data.bytes_to_human_readable)
status_swap_total = StatusItem(flask_babel.lazy_gettext('Total'), memory.swap_total,
                               formatter = data.bytes_to_human_readable)
status_swap_used = StatusItem(flask_babel.lazy_gettext('Used'), memory.swap_used,
                              formatter = data.bytes_to_human_readable)
status_swap_available = StatusItem(flask_babel.lazy_gettext('Available'), memory.swap_available,
                                   formatter = data.bytes_to_human_readable)
group_memory_ram.append(status_mem_total)
group_memory_ram.append(status_mem_used)
group_memory_ram.append(status_mem_available)
group_memory_swap.append(status_swap_total)
group_memory_swap.append(status_swap_used)
group_memory_swap.append(status_swap_available)
group_memory.append(group_memory_ram)
group_memory.append(group_memory_swap)

# Network.
status_hostname = StatusItem(flask_babel.lazy_gettext('Host Name'), network.hostname)
status_ip_external = StatusItem(flask_babel.lazy_gettext('External IP'),
                                network.external_ip_address)
status_ip_eth0 = StatusItem(flask_babel.lazy_gettext('Ethernet'), network.ip_address,
                            ['eth0', network.IPVersion.v4])
status_ip_wlan0 = StatusItem(flask_babel.lazy_gettext('WLAN'), network.ip_address,
                             ['wlan0', network.IPVersion.v4])
group_network.append(status_hostname)
group_network.append(status_ip_external)
group_network.append(group_network_internal_ip)
group_network_internal_ip.append(status_ip_eth0)
group_network_internal_ip.append(status_ip_wlan0)

Statuses = [group_os, group_users, group_cpu, group_storage, group_memory, group_network]
