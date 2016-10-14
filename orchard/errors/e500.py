# -*- coding: utf-8 -*-

"""
    This module sets up the view for handling ``500 Internal Server Error`` errors.
"""

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
            Display the error page.

            :return: A page explaining the error.
        """
        return flask.render_template('errors/500.html')

Error500View.register(blueprint)
