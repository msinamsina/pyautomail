Tutorial
========

.. note::
   To install automail please see :ref:`installation <installation>`

Base usage
==========

Below is a Python script that demonstrates how to send a single email:


.. literalinclude:: ../../examples/base-usage.py
   :language: python
   :end-before: Creating a sender object


.. literalinclude:: ../../examples/base-usage.py
   :language: python
   :start-after: Creating a sender object
   :end-before: Set the template

CLI Usage
---------

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