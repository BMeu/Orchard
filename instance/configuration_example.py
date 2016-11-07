# -*- coding: utf-8 -*-

"""
    Instance configuration, possibly overwriting default values.
"""


class Configuration:
    """
        Instance specific configurations for |projectname| that should not be shared with anyone
        else (e.g. because of passwords).

        You can overwrite any of the values from :mod:`orchard.configuration` in this class.
    """

    BABEL_DEFAULT_LOCALE = 'en'
    """
        The default language if not other could be determined.

        :type: str
    """

    BABEL_DEFAULT_TIMEZONE = 'UTC'
    """
        The default timezone when formatting dates.

        :type: str
    """

    ADMINS = ['admin@example.com']
    """
        A list of email addresses of all administrators who will be notified on program failures.

        :type: List[str]
    """

    MAIL_FROM = 'no-reply@example.com'
    """
        The address appearing as the sender of all mails.

        :type: str
    """

    MAIL_SERVER = 'localhost'
    """
        An SMTP mail server used for sending all mails.

        :type: str | None
    """

    MAIL_PORT = 25
    """
        The port under which the :attr:`.MAIL_SERVER` is accessible.

        :type: int
    """

    MAIL_SSL = False
    """
        If set to True, the :attr:`.MAIL_SERVER` will be accessed via SSL.

        :type: bool
    """

    MAIL_USERNAME = None
    """
        A user on the :attr:`.MAIL_SERVER`. If no user is required to send mails, this can be set to
        ``None``.

        :type: str | None
    """

    MAIL_PASSWORD = None
    """
        The password for the :attr:`.MAIL_USERNAME`. If no password is required, this can be set to
        ``None``.

        :type: str | None
    """

    SECRET_KEY = ''
    """
        A long, random, and secret string used to secure sessions.

        :type: str
    """
