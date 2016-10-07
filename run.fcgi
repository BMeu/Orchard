#!venv/bin/python
# -*- coding: utf-8 -*-

"""
    WSGI script to run Orchard on a real server like Apache or nginx.
"""

import flup.server.fcgi
import orchard

if __name__ == '__main__':
    app = orchard.create_app('Production')
    flup.server.fcgi.WSGIServer(app).run()
