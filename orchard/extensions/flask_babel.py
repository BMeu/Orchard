# -*- coding: utf-8 -*-

"""
    Initialize the Babel extension.
"""

import flask
import flask_babel

babel = flask_babel.Babel()


@babel.localeselector
def _get_locale() -> str:
    """
        Determine the locale best suited for the current user.

        :return: The locale code.
    """
    languages = flask.current_app.config['LANGUAGES'].keys()
    locale = flask.request.accept_languages.best_match(languages)

    # If no locale could be determined, fall back to the default.
    if locale is None:
        locale = flask.current_app.config['BABEL_DEFAULT_LOCALE']

    return locale
