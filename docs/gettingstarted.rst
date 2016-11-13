.. _GettingStarted:

Getting Started
===============

Getting |projectname| to run is fairly simple if you follow this guide. It may seem much, but is
quickly done (unless you have to compile Python 3.5 yourself---that might take some time).

This guide assumes you are running Raspbian. If you are using another OS, some of the commands
(especially when installing packages) might differ.

System Requirements
-------------------

* A Raspberry Pi (duh!), running Raspbian
* Python 3.5
* A webserver like Apache or nginx with FCGI support
* Optionally: Git

Python 3.5 is a bit of a problem right now (November 2016) if you are using Raspbian, as it is not
yet available there. Thus, we will have to compile it ourselves.

You should have a bit of experience using the terminal.

|projectname| should run on any other Linux, but the default configuration of system
information relies on Raspbian.

Installing Python 3.5
~~~~~~~~~~~~~~~~~~~~~

If you have Python 3.5 already installed on your Raspberry, you can skip this step. If you are
not sure, try running it:

.. code-block:: bash

    $ python3.5

If you get an error message like ``Command not found``, you will have to install it yourself (if
you are lucky, it will be available in the repositories by the time you are reading this, try
``sudo apt-get update; sudo apt-get install python3.5``, otherwise follow the following steps).
This might take some time...

1. Install the required build-tools (some might already be installed on your system).

   .. code-block:: bash

        $ sudo apt-get update
        $ sudo apt-get install build-essential tk-dev
        $ sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev
        $ sudo apt-get install libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
        $ sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

   If one of the packages cannot be found, try a newer version number (e.g. ``libdb5.4-dev``
   instead of ``libdb5.3-dev``).

2. Download and install Python 3.5. When downloading the source code, select the most recent release
   of Python 3.5, available on the `official site <https://www.python.org/downloads/source/>`_.
   Adjust the file names accordingly.

   .. code-block:: bash

        $ wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
        $ tar zxvf Python-3.5.2.tgz
        $ cd Python-3.5.2
        $ ./configure --prefix=/usr/local/opt/python-3.5.2
        $ make
        $ sudo make install

3. Make the compiled binaries globally available.

   .. code-block:: bash

        $ sudo ln -s /usr/local/opt/python-3.5.2/bin/pydoc3.5 /usr/bin/pydoc3.5
        $ sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5 /usr/bin/python3.5
        $ sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5m /usr/bin/python3.5m
        $ sudo ln -s /usr/local/opt/python-3.5.2/bin/pyvenv-3.5 /usr/bin/pyvenv-3.5
        $ sudo ln -s /usr/local/opt/python-3.5.2/bin/pip3.5 /usr/bin/pip3.5

   You should now have a fully working Python 3.5 installation on your Raspberry Pi!

4. Optionally: Delete the source code and uninstall the previously installed packages. When
   uninstalling the packages, make sure you only remove those that were not previously installed
   on your system. Also, remember to adjust version numbers if necesarry.

   .. code-block:: bash

        $ sudo rm -r Python-3.5.2
        $ rm Python-3.5.2.tgz
        $ sudo apt-get --purge remove build-essential tk-dev
        $ sudo apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
        $ sudo apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
        $ sudo apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
        $ sudo apt-get autoremove
        $ sudo apt-get clean

This guide is pretty much taken from the following tutorial:
https://liudr.wordpress.com/2016/02/04/install-python-on-raspberry-pi-or-debian/

Installing Orchard
------------------

We will install |projectname| to ``/opt/orchard`` using Git. You can use any other path you like,
just remember to adjust it in the steps accordingly. Git will allow us to easily update
|projectname| in the future, but if you want, you can download
`the latest archived release <https://github.com/BMeu/Orchard/releases>`_ using ``wget`` and
unpack it in the installation directory.

1. Create the installation directory and clone |projectname| from Github.

   .. code-block:: bash

        $ sudo mkdir /opt/orchard
        $ cd /opt/orchard
        $ sudo chown -R $USER .
        $ git clone https://github.com/BMeu/Orchard.git .

2. Create the virtual environment and install the required Python packages. You must not change
   the name of the virtual environment!

   .. code-block:: bash

        $ pyvenv-3.5 venv
        $ source venv/bin/activate
        (venv) $ pip install -r requirements.txt

3. You can now edit the configuration of |projectname|. All available options are explained in
   full detail in the API documentation (:mod:`instance`, :mod:`orchard.configuration`).

   .. code-block:: bash

        (venv) $ cp instance/configuration_example.py instance/configuration.py
        (venv) $ cp instance/status_configuration_example.py instance/status_configuration.py
        (venv) $ nano instance/configuration.py

   Save the file using ``[Ctrl] + [O]``, confirm with ``[Enter]``, and exit ``[Ctrl] + [X]``.

4. Compile the translations.

   .. code-block:: bash

        (venv) $ ./manage.py babel compile

5. Optionally: If you want, you can run the tests and build the documentation to ensure
   |projectname| is working correctly (you will need to have the virtual environment activated!).

   .. code-block:: bash

        (venv) $ ./manage.py test
        (venv) $ ./manage.py doc

Congratulations, you have successfully installed |projectname|! All that is left to do is to
configure your webserver.

Configuring the Webserver
-------------------------

|projectname| uses the micro webdevelopment framework `Flask <http://flask.pocoo.org/>`_ which
comes with a build-in development server. However, this server is not suited for real-life usage.
Instead, you should use a real webserver like `Apache <https://www.apache.org/>`_ or
`nginx <https://nginx.org/>`_. |projectname| comes with a WSGI script (``run.fcgi``) the server
can use to access the application.

This guide assumes you have been following the steps above and your webserver is already installed
(if this is not the case, use one of the many tutorials out there in the Internet). If you are not
currently within the installation directory, change into it.

.. code-block:: bash

    $ cd /opt/orchard

Apache
~~~~~~

1. Install the Apache FCGI module (if it is already installed, you can skip this step).

   .. code-block:: bash

        $ sudo apt-get update
        $ sudo apt-get install libapache2-mod-fcgid
        $ sudo a2enmod fcgid
        $ sudo service apache2 restart

2. We want Apache to have access to our files, but we don't want to make the Apache user (usually
   ``www-data``) the owner of the files as this would prevent us from easily updating |projectname|
   using Git. Therefore, we will create a new user group for ourselves and the Apache user and set
   the group of |projectname| to this new one.

   .. code-block:: bash

        $ sudo groupadd orchard
        $ sudo usermod -a -G orchard $USER
        $ sudo usermod -a -G orchard www-data
        $ chgrp -R orchard .
        $ chmod -R g+w .
        $ chmod g+s `find . -type d`

3. |projectname| uses the script ``/opt/vc/bin/vcgencmd`` to retrieve some information on the
   system. However, this script requires root permissions to be executed. Therefore, we will allow
   our newly created group to execute exactly this script (and nothing else) using ``sudo`` without
   asking for a password.

   Open the ``sudoers`` file:

   .. code-block:: bash

        $ sudo visudo

   Then add the following lines at the end of the file; make sure to leave the very last line blank:

   .. code-block:: text

         # Allow the Orchard group to execute the vcgencmd script.
         %orchard ALL=NOPASSWD: /opt/vc/bin/vcgencmd

   Save and exit the file (if you are using ``nano`` as your default editor, ``[Ctrl] + [O]``,
   ``[Enter]``, and ``[Ctrl] + [X]``).

4. Tell Apache where to find |projectname|.

   a. If you do not use SSL, open the following file:

      .. code-block:: bash

         $ sudo nano /etc/apache2/sites-available/000-default.conf

      If you are using SSL, open this file instead:

      .. code-block:: bash

         $ sudo nano /etc/apache2/sites-available/default-ssl.conf


   b. Paste the following configuration somewhere into the file between the
      ``<VirtualHost></VirtualHost>`` tags (remember to adjust the paths to your needs).

      .. code-block:: apache

           ScriptAlias /orchard /opt/orchard/run.fcgi/
           <Directory /opt/orchard/>
               Options +ExecCGI
               Require all granted
           </Directory>

           Alias /orchard/static /opt/orchard/orchard/static
           <Directory /opt/orchard/orchard/static/>
               Require all granted
           </Directory>

   Save the file using ``[Ctrl] + [O]``, confirm with ``[Enter]``, and exit ``[Ctrl] + [X]``.

5. Reload the server:

   .. code-block:: bash

        $ sudo service apache2 reload

You should now be able to access |projectname| under the address of your Raspberry Pi at
``/orchard`` in your browser. This finishes the installation!

What if you want |projectname| to be your home page (i.e. have it available under ``/``)? This is a
little bit more tricky. Simply setting the ``ScriptAlias`` line in step 4b to
``ScriptAlias / /opt/orchard.run.fcgi/`` would result in all of your other URLs being consumed by
|projectname| and thus not working as expected anymore. What we want is |projectname| to be
called if the requested URL does not exist on the server---that's exactly what the
``ErrorDocument 404`` directive is for! Unfortunately, this won't let us append the original
request URL to the error document, so we will use a combination of ``ErrorDocument`` and the
``rewrite`` module.

First, enable the rewrite module (if needed):

.. code-block:: bash

    $ sudo a2enmod rewrite

Now paste the following lines into the Apache configuration file after the lines you have added
in step 4:

.. code-block:: apache

    ErrorDocument 404 /orchard

    RewriteEngine on
    RewriteCond %{ENV:REDIRECT_STATUS} "=404"
    RewriteRule (.*) /opt/orchard/run.fcgi%{ENV:REDIRECT_URL} [L]

    RewriteCond %{REQUEST_FILENAME} ^/$
    RewriteRule (.*) /opt/orchard/run.fcgi/ [L]

What does it do? Any requests that would result in a ``404 Not Found`` error will be caught by
the first line and handled by ``/orchard``. This will also automatically set the environment
variables ``REDIRECT_STATUS`` to ``404`` and ``REDIRECT_URL`` to the requested URL, respectively.
The second line simply enables the rewriting. The third line ensures the following rewrite rule
will only be applied if the request has triggered a ``404`` error, using the ``REDIRECT_STATUS``
environment variable. The rewrite rule in the fourth line rewrites all requests (if they have
triggered a ``404`` error) to the |projectname| script, adding the orginal requested URL which
then can be handled by the script (the ``[L]`` stops any further processing of the request by the
rewrite module). The last two lines simply rewrite all requests to ``/`` to the |projectname|
script, so |projectname| will actually be opened if you access ``/`` on your server. Don't forget
to reload the server:

.. code-block:: bash

    $ sudo service apache2 reload

nginx
~~~~~

.. todo::

   Add a guide for nginx.
