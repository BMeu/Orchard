# -*- coding: utf-8 -*-

"""
    Simple testing blueprint. Will be deleted once real functionality is added.
"""

import flask
import flask_babel
import flask_classful

views = flask.Blueprint('views', __name__)


class IndexView(flask_classful.FlaskView):
    """
        A simple home page.
    """
    route_base = '/'

    # noinspection PyMethodMayBeStatic
    def index(self) -> str:
        """
            Display a simple greeting.

            :return: A message to all visitors.
        """
        return flask_babel.gettext('Welcome to the Orchard!')

    # noinspection PyMethodMayBeStatic
    def get(self, name: str) -> str:
        """
            Display a simple personalized greeting.

            :param name: The name of the visitor.
            :return: A message to the visitor.
        """
        return flask_babel.gettext('Welcome to the Orchard, %(name)s!', name = name)


IndexView.register(views)
