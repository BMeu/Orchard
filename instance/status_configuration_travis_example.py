# -*- coding: utf-8 -*-

"""
    Configuration of system status items and groups.
"""

import flask_babel

from orchard.system_status import StatusGroup, StatusItem
from orchard.system_status.formatters import data
from orchard.system_status.formatters import os as formatter_os
from orchard.system_status.system import cpu, memory, network, os, storage

# Create the status groups.
group_cpu = StatusGroup(flask_babel.gettext('CPU'))
group_memory = StatusGroup(flask_babel.gettext('Memory'))
group_network = StatusGroup(flask_babel.gettext('Network'))
group_os = StatusGroup(flask_babel.gettext('Operating System'))
group_storage = StatusGroup(flask_babel.gettext('Storage'))
group_users = StatusGroup(flask_babel.gettext('Users'))

# Operating System.
status_kernel = StatusItem(flask_babel.gettext('Kernel'), os.kernel_version,
                           formatter = formatter_os.kernel)
status_boottime = StatusItem(flask_babel.gettext('Boot Time'), os.boot_time,
                             formatter = flask_babel.format_datetime)
status_runtime = StatusItem(flask_babel.gettext('Runtime'), os.run_time,
                            formatter = flask_babel.format_timedelta)
status_current_time = StatusItem(flask_babel.gettext('Current Time'), os.current_time,
                                 formatter = flask_babel.format_datetime)
group_os.append(status_kernel)
group_os.append(status_boottime)
group_os.append(status_runtime)
group_os.append(status_current_time)

# Users.
status_current_logins = StatusItem(flask_babel.gettext('Current Logins'), os.current_logins,
                                   formatter = formatter_os.current_logins)
status_last_login = StatusItem(flask_babel.gettext('Last Login'), os.last_login,
                               formatter = formatter_os.last_login)
group_users.append(status_current_logins)
group_users.append(status_last_login)

# CPU.
status_processes = StatusItem(flask_babel.gettext('Running Processes'), os.running_processes)
status_load_one = StatusItem(flask_babel.gettext('Load (1-minute average)'), cpu.load,
                             [cpu.LoadPeriods.one])
status_load_five = StatusItem(flask_babel.gettext('Load (5-minute average)'), cpu.load,
                              [cpu.LoadPeriods.five])
status_load_fifteen = StatusItem(flask_babel.gettext('Load (15-minute average)'), cpu.load,
                                 [cpu.LoadPeriods.fifteen])
group_cpu.append(status_processes)
group_cpu.append(status_load_one)
group_cpu.append(status_load_five)
group_cpu.append(status_load_fifteen)

# Storage.
status_storage_total = StatusItem(flask_babel.gettext('Total'), storage.total,
                                  formatter = data.bytes_to_human_readable)
status_storage_used = StatusItem(flask_babel.gettext('Used'), storage.used,
                                 formatter = data.bytes_to_human_readable)
status_storage_available = StatusItem(flask_babel.gettext('Available'), storage.available,
                                      formatter = data.bytes_to_human_readable)
group_storage.append(status_storage_total)
group_storage.append(status_storage_used)
group_storage.append(status_storage_available)

# Memory.
status_mem_total = StatusItem(flask_babel.gettext('Total'), memory.total,
                              formatter = data.bytes_to_human_readable)
status_mem_used = StatusItem(flask_babel.gettext('Used'), memory.used,
                             formatter = data.bytes_to_human_readable)
status_mem_available = StatusItem(flask_babel.gettext('Free'), memory.free,
                                  formatter = data.bytes_to_human_readable)
status_swap_total = StatusItem(flask_babel.gettext('Swap: Total'), memory.swap_total,
                               formatter = data.bytes_to_human_readable)
status_swap_used = StatusItem(flask_babel.gettext('Swap: Used'), memory.swap_used,
                              formatter = data.bytes_to_human_readable)
status_swap_available = StatusItem(flask_babel.gettext('Swap: Available'), memory.swap_available,
                                   formatter = data.bytes_to_human_readable)
group_memory.append(status_mem_total)
group_memory.append(status_mem_used)
group_memory.append(status_mem_available)
group_memory.append(status_swap_total)
group_memory.append(status_swap_used)
group_memory.append(status_swap_available)

# Network.
status_ip_external = StatusItem(flask_babel.gettext('External IP'), network.external_ip_address)
status_ip_eth0 = StatusItem(flask_babel.gettext('Internal IP (Ethernet)'), network.ip_address,
                            ['eth0', network.IPVersion.v4])
status_ip_wlan0 = StatusItem(flask_babel.gettext('Internal IP (WLAN)'), network.ip_address,
                             ['wlan0', network.IPVersion.v4])
group_network.append(status_ip_external)
group_network.append(status_ip_eth0)
group_network.append(status_ip_wlan0)

Statuses = [group_os, group_users, group_cpu, group_storage, group_memory, group_network]
