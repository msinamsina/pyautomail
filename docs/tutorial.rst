.. Automail documentation master file, created by
   sphinx-quickstart on Tue Jul 25 17:21:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorial
====================================

Installation
------------------------------------

download the source code from `github <git@github.com:msinamsina/automail.git>`_ and install it with
.. code-block:: bash

   $ git clone git@github.com:msinamsina/automail.git
   $ cd automail
   $ python setup.py install

.. note::

   This project is under active development.


Usage
------------------------------------

.. note::
   After installation, you can use the command line tool ``automail`` to send emails.

For sending emails, you need to do the following steps:
- register a new process
   .. code-block:: bash

      $ automail register your-email-address path-to-your-contact-list

   this command will return a process-id, which you will use to start the process.
- start the process
   .. code-block:: bash

      $ automail start process-id