# -*- coding: utf-8 -*-

"""
    This module exports functions to initialize the Flask application.
"""

import random
from typing import Callable, Dict

import flask
import flask_babel

import orchard.errors
import orchard.extensions
import orchard.system_status


def create_app(config: str = 'Development') -> flask.Flask:
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
    app = flask.Flask(name, instance_relative_config = True)
    app.config.from_object(config)
    app.config.from_object('instance.Configuration')

    # Always use English as default language during testing.
    if app.testing:  # pragma: no branch.
        app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    _configure_blueprints(app)
    _configure_context_processor(app)
    _configure_extensions(app)
    _configure_logging(app)
    _configure_request_handlers(app)

    return app


def _configure_blueprints(app: flask.Flask):
    """
        Register the blueprints.

        :param app: The application instance.
    """
    app.register_blueprint(orchard.errors.blueprint)
    app.register_blueprint(orchard.system_status.blueprint)


def _configure_context_processor(app: flask.Flask):
    """
        Set up the global context processors.

        :param app: The application instance.
    """

    @app.context_processor
    def inject_jinja2() -> Dict[str, Callable]:
        """
            Inject more functions into the scope of Jinja2 templates.

            :return: A dictionary
        """
        jinja2_functions = {
            'hasattr': hasattr,
            'random_int': random.randint
        }

        return jinja2_functions


def _configure_extensions(app: flask.Flask):
    """
        Register the extensions with the app and configure them as needed.

        :param app: The application instance.
    """
    orchard.extensions.babel.init_app(app)
    orchard.extensions.cache.init_app(app)


def _configure_logging(app: flask.Flask):  # pragma: no cover.
    """
        Set up a file and a mail logger, unless the app is being debugged or tested.

        :param app: The application instance.
    """
    if app.debug or app.testing:
        return

    # noinspection PyUnresolvedReferences
    import logging
    import logging.handlers
    import os

    # Set up the file logger.
    log_path = app.config['LOG_PATH']
    if not os.path.isdir(log_path):
        os.makedirs(log_path)

    log_file = os.path.join(log_path, '{file_name}.log'.format(file_name = app.name))
    log_format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    file_handler = logging.handlers.RotatingFileHandler(log_file, 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('{name} Startup'.format(name = app.config['PROJECT_NAME']))

    # Set up the mail logger.
    if app.config.get('MAIL_SERVER', '') == '':
        return

    credentials = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    server = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    sender = app.config['MAIL_FROM']
    receivers = app.config['ADMINS']
    subject = '{name} Failure'.format(name = app.config['PROJECT_NAME'])
    secure = None
    if app.config['MAIL_SSL']:
        secure = ()
    mail_handler = logging.handlers.SMTPHandler(server, sender, receivers, subject, credentials,
                                                secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


def _configure_request_handlers(app: flask.Flask):
    """
        Set up the global before and after request handlers.

        :param app: The application instance.
    """

    @app.before_request
    def before_request():
        """
            Set up a few things before handling the actual request.
        """
        flask.g.locale = flask_babel.get_locale()

        # Set a default title.
        flask.g.title = app.config['PROJECT_NAME']

    @app.after_request
    def after_request(response: flask.Response) -> flask.Response:
        """
            Modify the response after the request has been handled.

            :return: The modified response.
        """
        # http://www.gnuterrypratchett.com/
        response.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")

        return response
