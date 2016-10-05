#!venv/bin/python
# -*- coding: utf-8 -*-

"""
    A script to manage Orchard from the command line.

    Run
        ./orchard.py
    for usage information.
"""

import os
import sys

import click

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
click_context = dict(help_option_names = ['-h', '--help'])


@click.group(context_settings = click_context)
def main():
    """
        Manage Orchard from the command line.
    """
    pass


@main.command()
def lint():
    """
        Run a linter against the source code.
    """
    print('RUNNING LINTER.\n')

    import subprocess

    linter = subprocess.call(['flake8', '--ignore=E251', '--max-line-length=100',
                              '--count', 'orchard.py', 'orchard/', 'tests/'])

    if linter:
        print('\nFAILED')
    else:
        print('\nOK')

    sys.exit(1 if linter else 0)


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


@main.command()
@click.argument('module', required = False)
@click.option('-f', '--full-coverage', is_flag = True, default = False,
              help = 'Record coverage statistics for the entire source code, even if only a single '
                     'module is being tested.')
def test(module, full_coverage):
    """
        Execute all tests and report code coverage.

        \b
        [MODULE]    The full module name (without orchard at the beginning)
                    to execute only its tests.
    """
    import coverage
    import shutil
    import unittest

    start_directory = './tests'
    coverage_file = ['*/*.py']
    test_file = '*_test.py'
    if module:
        modules = module.split('.')

        # The source file is simply the module within the main package.
        if not full_coverage:
            coverage_file = ['./orchard/{0}.py'.format('/'.join(modules))]

        # If the module to test is the __init__ module, its test will be the package's name.
        if modules[-1] == '__init__':
            try:
                modules[-1] = modules[-2]
            except IndexError:
                modules[-1] = 'orchard'
        test_file = '{0}_test.py'.format(modules.pop())
        start_directory = './tests/{0}'.format('/'.join(modules))

    # Start recording the code coverage.
    coverage_engine = coverage.coverage(branch = True, source = ['./orchard'],
                                        include = coverage_file, omit = ['./orchard/configuration'])
    coverage_engine.start()

    # Import the app and initialize it for testing.
    from orchard import app
    app.testing = True

    # Run the tests.
    tests = unittest.TestLoader().discover(start_directory, test_file)
    test_runner = unittest.TextTestRunner(verbosity = 2)
    test_result = test_runner.run(tests).wasSuccessful()

    # Create a fresh build directory if necessarry.
    build_directory = os.path.join(basedir, 'build/coverage')
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    # Stop the coverage engine and save the report.
    title = '{0} Coverage Report'.format('ORCHARD')
    coverage_engine.stop()
    coverage_engine.save()
    coverage_result = coverage_engine.html_report(directory = build_directory, title = title)
    coverage_engine.xml_report(outfile = build_directory + '/coverage.xml')
    print('\nAchieved total coverage: {0:0.1f}%'.format(coverage_result))
    print('Coverage report saved to {0}.'.format(os.path.join(basedir, build_directory)))
    coverage_engine.erase()

    sys.exit(0 if test_result else 1)


if __name__ == '__main__':
    main()
