# -*- coding: utf-8 -*-

"""
    This module sets up the view for handling ``500 Internal Server Error`` errors.
"""

import datetime

import flask
import flask_classful

from orchard.errors import blueprint


class Error500View(flask_classful.FlaskView):
    """
        View for ``500 Internal Server Error`` errors.
    """
    trailing_slash = False

    @blueprint.app_errorhandler(500)
    @blueprint.app_errorhandler(Exception)
    def index(self) -> str:
        """
            Display the error page for internal errors and send a mail to all administrators
            information them of this error.

            :return: A page explaining the error.
        """
        message = ('Time:      {time}\n' +
                   'Request:   {method} {path}\n' +
                   'Agent:     {agent_platform} | {agent_browser} {agent_browser_version}\n' +
                   'Raw Agent: {agent}\n\n'
                   ).format(time = datetime.datetime.now(),
                            method = flask.request.method,
                            path = flask.request.path,
                            agent_platform = flask.request.user_agent.platform,
                            agent_browser = flask.request.user_agent.browser,
                            agent_browser_version = flask.request.user_agent.version,
                            agent = flask.request.user_agent.string)

        flask.current_app.logger.exception(message)
        return flask.render_template('errors/500.html')

Error500View.register(blueprint)
