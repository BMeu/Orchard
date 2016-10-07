# -*- coding: utf-8 -*-

"""
    This module exports functions to initialize the Flask application.
"""

from flask import Flask

import orchard.views


def create_app(config: str = 'Development') -> Flask:
    """
        Create and initialize the Flask application.

        :param config: The name of the configuration class, valid values are ``Development``
                       (default), ``Production``, and ``Testing``.
        :return: The initialized Flask application.
    """
    configuration_values = {'Development', 'Production', 'Testing'}
    if config in configuration_values:
        config = 'orchard.configuration.{config}'.format(config = config)
    else:  # pragma: no cover.
        config = 'orchard.configuration.Development'

    name = __name__.split('.')[0]
    app = Flask(name, instance_relative_config = True)
    app.config.from_object(config)
    app.config.from_object('instance.Configuration')

    _configure_blueprints(app)

    return app


def _configure_blueprints(app: Flask):
    """
        Register the blueprints.

        :param app: The application instance.
    """
    app.register_blueprint(orchard.views.views)
