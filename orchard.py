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
from typing import Any, Dict, List

import click

available_tests = ['property', 'unit']
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
click_context = dict(help_option_names = ['-h', '--help'])


@click.group(context_settings = click_context)
def main():
    """
        Manage Orchard from the command line.
    """
    pass


@main.command()
@click.option('-b', '--build', is_flag = True, default = False, prompt = 'Empty the build folder?',
              help = 'Empty the build folder.')
@click.option('-p', '--hypothesis', is_flag = True, default = False,
              prompt = 'Empty the property test example database?',
              help = 'Empty the property test example database.')
@click.option('-d', '--dry-run', is_flag = True, default = False,
              help = 'Do not actually delete anything, but instead list all files and folders '
                     'that would be deleted.')
def clean(build: bool = False, hypothesis: bool = False, dry_run: bool = False):
    """
        Remove temporary files and folders.
    """
    os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Default'

    import shutil
    import orchard

    def get_deletable_paths_in_directory(directory: str) -> List[str]:
        """
            Get a list of all files and folders in a directory that can savely be deleted.

            :param directory: The directory in which files and folders will be deleted.
            :return: A list of all files and folders in the directory, except '.gitkeep' files.
        """
        return [os.path.join(directory, p) for p in os.listdir(directory) if p != '.gitkeep']

    delete_list = []

    # Empty the build folder.
    if build:
        delete_list.extend(get_deletable_paths_in_directory(orchard.app.config['BUILD_PATH']))

    # Empty the property test example database.
    if hypothesis:
        delete_list.extend(get_deletable_paths_in_directory(orchard.app.config['HYPOTHESIS_PATH']))

    if dry_run:
        print('\nFILES THAT WOULD BE DELETED:\n')
    else:
        print('\nDELETING...\n')

    # Delete the actual files (or at least print the files).
    for deletable in delete_list:
        print(deletable)

        if not dry_run:
            if os.path.isdir(deletable):
                shutil.rmtree(deletable)
            else:
                os.unlink(deletable)


@main.command()
def doc():
    """
        Build the documentation.
    """
    print('BUILDING DOCUMENTATION\n')
    os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Default'

    import shutil
    import subprocess
    import orchard

    # Directories.
    build_directory = os.path.join(orchard.app.config['BUILD_PATH'], 'docs')
    source_directory = 'docs'

    # Create a fresh build directory if necessarry.
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    built = subprocess.call(['sphinx-build', '-b', 'html', source_directory,
                             '{0}/html'.format(build_directory)]) == 0

    if built:
        print('\nOK')
    else:
        print('\nFAILED')

    sys.exit(0 if built else 1)


@main.command()
def lint():
    """
        Run a linter against the source code.
    """
    import subprocess

    print('RUNNING LINTER.\n')

    linter = subprocess.call(['flake8', '--ignore=E251', '--max-line-length=100',
                              '--count', 'orchard.py', 'orchard/', 'tests/'])

    if linter:
        print('\nFAILED')
    else:
        print('\nOK')

    sys.exit(1 if linter else 0)


@main.command()
@click.option('-p', '--production', is_flag = True, default = False,
              help = 'Run the server in production mode.')
@click.option('-a', '--profile', is_flag = True, default = False,
              help = 'Analyze the code execution using a profiler.')
def run(production: bool = False, profile: bool = False):
    """
        Run the server in debug mode.
    """
    host = '127.0.0.1'
    os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Development'
    if production:
        host = '0.0.0.0'
        os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Production'

    import orchard

    if profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        orchard.app.config['PROFILE'] = True
        orchard.app.wsgi_app = ProfilerMiddleware(orchard.app.wsgi_app, restrictions = [30])

    orchard.app.run(host = host)


@main.command()
def shell():
    """
        Start a Python shell.
    """
    import sys
    import werkzeug.script

    def create_context() -> Dict[str, Any]:
        """
            Create a context for the interactive shell.

            :return: A dictionary of object instances.
        """
        os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Production'
        import flask
        import orchard

        app_context = orchard.app.app_context()
        app_context.push()

        return dict(app = orchard.app, g = flask.g)

    keys = create_context()
    banner = ('Python {version} on {platform}\n' +
              'Type "help", "copyright", "credits" or "license" for more information.\n' +
              'Type "exit()" to quit the session.\n\n' +
              'App: {app_name}\n' +
              'Instance: {instance_path}\n'
              'Exported objects: {exported_objects}\n')
    banner = banner.format(version = sys.version, platform = sys.platform,
                           app_name = keys['app'].name, instance_path = keys['app'].instance_path,
                           exported_objects = ', '.join(create_context().keys()))

    werkzeug.script.make_shell(create_context, banner = banner)()


@main.command()
@click.argument('module', required = False)
@click.option('-f', '--full-coverage', is_flag = True, default = False,
              help = 'Record coverage statistics for the entire source code, even if only a single '
                     'module is being tested.')
@click.option('-t', '--test-types', type = click.Choice(available_tests), multiple = True,
              help = 'Run only the specified types of tests.')
def test(module: str, full_coverage: bool, test_types: str):
    """
        Execute all tests and report code coverage.

        \b
        [MODULE]    The full module name (without orchard at the beginning)
                    to execute only its tests.
    """
    import coverage
    import shutil
    import unittest

    # If no specific tests are requested, run all.
    if not test_types:
        test_types = tuple(available_tests)

    # Determine which modules to test.
    start_directory = './tests/{test_type}'
    coverage_file = ['*/*.py']
    test_file = '*_{test_type}_test.py'
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
        test_file = '{module}_{{test_type}}_test.py'.format(module = modules.pop())
        start_directory = './tests/{{test_type}}/{module}'.format(module = '/'.join(modules))

    # Start recording the code coverage.
    coverage_engine = coverage.coverage(branch = True, source = ['./orchard'],
                                        include = coverage_file, omit = ['./orchard/configuration'])
    coverage_engine.start()

    # Import the app and initialize it for testing.
    os.environ['ORCHARD_CONFIGURATION'] = 'orchard.configuration.Testing'
    import orchard

    # Set the directory where Hypothesis saves its files.
    import hypothesis.configuration
    hypothesis.configuration.set_hypothesis_home_dir(orchard.app.config['HYPOTHESIS_PATH'])

    # Run the specified tests.
    total_test_result = True
    for test_type in test_types:
        print('Running {test_type} tests.'.format(test_type = test_type).upper())
        directory = start_directory.format(test_type = test_type)

        tests = unittest.TestLoader().discover(directory, test_file.format(test_type = test_type))
        test_runner = unittest.TextTestRunner(verbosity = 2)
        test_result = test_runner.run(tests).wasSuccessful()

        total_test_result = total_test_result and test_result

        print('\n')

    # Create a fresh build directory if necessarry.
    build_directory = os.path.join(orchard.app.config['BUILD_PATH'], 'coverage')
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)

    # Stop the coverage engine and save the report.
    title = '{name} Coverage Report'.format(name = orchard.app.config['PROJECT_NAME'])
    coverage_engine.stop()
    coverage_engine.save()
    coverage_result = coverage_engine.html_report(directory = build_directory, title = title)
    coverage_engine.xml_report(outfile = build_directory + '/coverage.xml')
    print('\nAchieved total coverage: {0:0.1f}%'.format(coverage_result))
    print('Coverage report saved to {0}.'.format(os.path.join(basedir, build_directory)))
    coverage_engine.erase()

    sys.exit(0 if total_test_result else 1)


if __name__ == '__main__':
    main()
