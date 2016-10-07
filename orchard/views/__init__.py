# -*- coding: utf-8 -*-

"""
    Simple testing blueprint. Will be deleted once real functionality is added.
"""

import flask

views = flask.Blueprint('views', __name__)


@views.route("/")
@views.route("/<string:name>")
def index(name: str = None) -> str:
    """
        Display a simple greeting.

        :param name: The name of the visitor.
        :return: A message to all visitors.
    """
    greeting = 'Welcome to the Orchard!'
    if name is not None:
        greeting = 'Welcome to the Orchard, {name}!'.format(name = name)

    return greeting
