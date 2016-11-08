# -*- coding: utf-8 -*-

"""
    This module sets up the view for handling ``403 Forbidden`` errors.
"""

import flask
import flask_classful

from orchard.errors import blueprint


class Error403View(flask_classful.FlaskView):
    """
        View for ``403 Forbidden`` errors.
    """
    trailing_slash = False

    @blueprint.app_errorhandler(403)
    def index(self) -> str:
        """
            Display the error page.

            :return: A page explaining the error.
        """
        return flask.render_template('errors/403.html')

Error403View.register(blueprint)
