User Guide
==========

Right now, the usage of |projectname| is straight forward: open it in your browser and enjoy all
the information you get!

Configuring Which Statuses to Display
-------------------------------------

If you have followed the :ref:`GettingStarted` guide, you will have created a file
``status_configuration.py`` within your ``instance`` folder based on the example file. This
default configuration will provide you with the following information:

* Operating System:

  * Kernel version, including its compile time
  * GPU firmware, including its compile time
  * System boot time
  * System run time
  * Current time

* Users:

  * Number of currently logged in users
  * Name, host, and login time of the last user who logged in

* CPU:

  * Temperature in °C
  * Number of running processes
  * Load:

    * 1-minute average
    * 5-minute average
    * 15-minute average

* Storage:

  * Total
  * Used
  * Free

* Memory:

  * RAM:

    * Total
    * Used
    * Free

  * Swap:

    * Total
    * Used
    * Free

* Network:

  * Hostname
  * External IP
  * Internal IP (IPv4):

    * Ethernet (interface ``eth0``)
    * WLAN (interface ``wlan0``)

If you want to change this configuration (e.g. have the temperature in °F, or display IPv6
addresses as well), you will have to edit ``instance/status_configuration.py``:

.. code-block:: bash

    $ nano instance/status_configuration.py

Here, you can configure your own status groups and items. Groups allow up to one sub-group, but
you can add as many sub-groups and items to one group, and as many groups to the overview as you
wish. The module must export a variables named ``Statuses`` which is a list of all main
``StatusGroup`` instances. For more information on how to configure status groups and items, refer
to appropiate section of the API (:ref:`APISTatus`).

.. admonition:: Example

    If you want the temperatue in °F instead of °C, change the following line

    .. code-block:: python

        status_temperature = StatusItem(flask_babel.lazy_gettext('Temperature'),
                                        cpu.temperatue,
                                        formatter = temperature.celsius)

    to

    .. code-block:: python

        status_temperature = StatusItem(flask_babel.lazy_gettext('Temperature'),
                                        cpu.temperatue,
                                        formatter = temperature.celsius_to_fahrenheit)
