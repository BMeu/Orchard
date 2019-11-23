# -*- coding: utf-8 -*-

"""
    This module sets up the view for an overview of system status information.
"""

import flask
import flask_classful

import instance.status_configuration
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

        return flask.render_template('system_status/overview.html',
                                     statuses = instance.status_configuration.Statuses)


OverviewView.register(blueprint)
