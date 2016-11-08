# -*- coding: utf-8 -*-

"""
    This module sets up the view for handling ``400 Bad Request`` errors.
"""

import flask
import flask_classful

from orchard.errors import blueprint


class Error400View(flask_classful.FlaskView):
    """
        View for ``400 Bad Request`` errors.
    """
    trailing_slash = False

    @blueprint.app_errorhandler(400)
    def index(self) -> str:
        """
            Display the error page.

            :return: A page explaining the error.
        """
        return flask.render_template('errors/400.html')

Error400View.register(blueprint)
