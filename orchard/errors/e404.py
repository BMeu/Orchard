# -*- coding: utf-8 -*-

"""
    This module sets up the view for handling ``404 Not Found`` errors.
"""

import flask
import flask_classful

from orchard.errors import blueprint


class Error404View(flask_classful.FlaskView):
    """
        View for ``404 Not Found`` errors.
    """

    @blueprint.app_errorhandler(404)
    def index(self) -> str:
        """
            Display the error page.

            :return: A page explaining the error.
        """
        return flask.render_template('errors/404.html')

Error404View.register(blueprint)
