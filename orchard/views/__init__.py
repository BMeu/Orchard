# -*- coding: utf-8 -*-

"""
    Simple testing blueprint. Will be deleted once real functionality is added.
"""

import flask
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

            :return: The home page with a message to all visitors.
        """
        return flask.render_template('index.html')

    # noinspection PyMethodMayBeStatic
    def get(self, name: str) -> str:
        """
            Display a simple personalized greeting.

            :param name: The name of the visitor.
            :return: The home page with a message to the visitor.
        """
        if name == 'BMeu':
            flask.abort(500)
        elif name == 'BMeu2':
            raise ValueError

        return flask.render_template('index.html', name = name)


IndexView.register(views)
