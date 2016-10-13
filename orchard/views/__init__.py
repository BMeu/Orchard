# -*- coding: utf-8 -*-

"""
    Simple testing blueprint. Will be deleted once real functionality is added.
"""

import flask
import flask_babel

views = flask.Blueprint('views', __name__)


@views.route("/")
@views.route("/<string:name>")
def index(name: str = None) -> str:
    """
        Display a simple greeting.

        :param name: The name of the visitor.
        :return: A message to all visitors.
    """
    greeting = flask_babel.gettext('Welcome to the Orchard!')
    if name is not None:
        greeting = flask_babel.gettext('Welcome to the Orchard, %(name)s!', name = name)

    return greeting
