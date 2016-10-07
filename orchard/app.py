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
    _configure_logging(app)

    return app


def _configure_blueprints(app: Flask):
    """
        Register the blueprints.

        :param app: The application instance.
    """
    app.register_blueprint(orchard.views.views)


def _configure_logging(app: Flask):  # pragma: no cover.
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
    sender = 'no-replay@{host}'.format(host = app.config['MAIL_SERVER'])
    receivers = app.config['ADMINS']
    subject = '{name} Failure'.format(name = app.config['PROJECT_NAME'])
    mail_handler = logging.handlers.SMTPHandler(server, sender, receivers, subject, credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
