# -*- coding: utf-8 -*-

"""
    The main package of orchard.
"""

from flask import Flask
app = Flask(__name__)


@app.route("/")
def index() -> str:
    """
        Display a simple greeting.

        :return: A message to all visitors.
    """
    return "Welcome to the Orchard!"
