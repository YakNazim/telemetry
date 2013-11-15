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

Make sure you have python and pip: ::

    $ sudo apt-get install python2.7 python-pip virtualenvwrapper

Create an environment to run in: ::

    $ mkvirtualenv psas-telemetry

Install python dependencies: ::

    $ pip install -r requirements.txt


Running
=======

Start the telemetry server ::

    $ ./telemetry.py

Then point a browser to http://localhost:8080/
