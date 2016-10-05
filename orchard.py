#!venv/bin/python
# -*- coding: utf-8 -*-

"""
    A script to manage Orchard from the command line.

    Run
        ./orchard.py
    for usage information.
"""

import click

click_context = dict(help_option_names = ['-h', '--help'])


@click.group(context_settings = click_context)
def main():
    """
        Manage Orchard from the command line.
    """
    pass


@main.command()
@click.option('-p', '--production', 'mode', flag_value = 'production',
              help = 'Run the server in production mode.')
@click.option('-a', '--profile', 'mode', flag_value = 'profile',
              help = 'Analyze the code execution using a profiler.')
def run(mode):
    """
        Run the server in debug mode.
    """
    from orchard import app

    # Wit profiler.
    if mode == 'profile':
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
        app.run(debug = True)
        return

    # Without profiler.
    host = '127.0.0.1'
    debug = True
    if mode == 'production':
        host = '0.0.0.0'
        debug = False

    app.run(host = host, debug = debug)


if __name__ == '__main__':
    main()
