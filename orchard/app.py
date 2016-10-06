# -*- coding: utf-8 -*-

"""
    This module initializes the application.

    .. warning:: Importing this module will directly initialize the app!
"""

import os

from flask import Flask


app = Flask(__name__, instance_relative_config = True)

# Load the configuration from the environment or exit with an error message.
configuration = os.environ.get('ORCHARD_CONFIGURATION')
if configuration is None:  # pragma: no cover.
    import sys
    print('Error: No configuration specified. You did not provide the ORCHARD_CONFIGURATION '
          'environment variable.')
    sys.exit(1)

# Load the specified configuration.
app.config.from_object(configuration)
app.config.from_object('instance.Configuration')


@app.route("/")
def index() -> str:
    """
        Display a simple greeting.

        :return: A message to all visitors.
    """
    return "Welcome to the Orchard!"