# -*- coding: utf-8 -*-

"""
    This module sets up the view for an overview of system status information.
"""

import flask
import flask_classful

from orchard.system_status import blueprint


class OverviewView(flask_classful.FlaskView):
    """
        View for an overview of system status information.
    """
    route_base = '/'

    # noinspection PyMethodMayBeStatic
    def index(self) -> str:
        """
            Display a page with an overview of all configured system statuses.

            :return: A page with a table of all configured system statuses.
        """
        status = {
            'System': {
                'Kernel': 'Linux raspberry 4.4.30-v7+ #919, November 1st, 2016, 16:57:28h',
                'GPU': 'f74adfcae00b721627eab44590728c13860bcbc2, October 25th, 2016, 16:03:42h',
                'Runtime': '3 days, 02:28:39 hours'
            },
            'Users': {
                'SSH Logins': 'Two users are currently logged in.',
                'Last Login': 'November 8th, 2016, 00:07:18h, on fe80::108e:d4a8:'
            }
        }

        return flask.render_template('index.html', status = status)

OverviewView.register(blueprint)
