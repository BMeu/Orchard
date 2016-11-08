# -*- coding: utf-8 -*-

"""
    Configuration of system status items and groups.
"""

import flask_babel

from orchard.system_status import StatusGroup, StatusItem

group_system = StatusGroup(flask_babel.gettext('System'))
status_kernel = StatusItem(flask_babel.gettext('Kernel'), str,
                           ['Linux raspberry 4.4.30-v7+ #919, November 1st, 2016, 16:57:28h'])
status_gpu = StatusItem(flask_babel.gettext('GPU'), str,
                        ['f74adfcae00b721627eab44590728c13860bcbc2, October 25th, 2016, 16:03:42h'])
status_runtime = StatusItem(flask_babel.gettext('Runtime'), str, ['3 days, 02:28:39 hours'])
group_system.append(status_kernel)
group_system.append(status_gpu)
group_system.append(status_runtime)

group_users = StatusGroup(flask_babel.gettext('Users'))
status_logins = StatusItem(flask_babel.gettext('SSH Logins'), str,
                           ['Two users are currently logged in.'])
status_last_login = StatusItem(flask_babel.gettext('Last Login'), str,
                               ['November 8th, 2016, 00:07:18h, on fe80::108e:d4a8:'])
group_users.append(status_logins)
group_users.append(status_last_login)

Statuses = [group_system, group_users]
