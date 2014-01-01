.. _quickstart:

==========
Quickstart
==========

If you just want to see telemetry, point your browser at a running instance of
the server (for instance at a launch we will be running a server in mission
control)

To install locally follow these instructions:


Installing
==========

Read about `python virualenv's! <http://blog.fruiapps.com/2012/06/An-introductory-tutorial-to-python-virtualenv-and-virtualenvwrapper>`_

Make sure you have python and pip ::

    $ sudo apt-get install python2.7 python-pip virtualenvwrapper

.. note:: If this is your first time using python virtual environments,
          remember to kill your shell and open a new one after installing
          virtualenvwrapper for the first time (you only have to do this
          once).

To build the javascript you need coffeescript_::

    $ sudo apt-get install nodejs npm

Install globablly, since you might want this for other projects.::

    $ sudo npm install -g coffee-script

Now you can build the js::

    $ make build

For the server, create a python environment to run in::

    $ mkvirtualenv psas-telemetry

Install python dependencies::

    (psas-telemetry)$ pip install -r requirements.txt


Running
=======

Start the telemetry server.  If you changed some scripts, don't forget to
rerun `make build`.::

    (psas-telemetry)$ ./telemetry.py


Usage
=====

Once the rocket is sending data and the backend server is running, simply
navigate to http://localhost:8080 to start seeing data.


.. _coffeescript: http://psas.pdx.edu/
