Tutorial
========

.. note::
   To install pyautomail please see :ref:`installation <installation>`

Config file
-----------

Config files have several sections with different attributes, which are described below.

    - ``[smtp]``: SMTP server settings
        - ``host``: SMTP server host
        - ``port``: SMTP server port
        - ``is_test``: If ``True``, emails will not be sent
    - ``[account]``: Email settings
        - ``user``: Email user
        - ``password``: Email password
    - ``[log]``: Logging settings
        - ``level``: Logging level 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL
        - ``file``: Log file path

.. literalinclude:: ../../examples/assets/config.cfg
   :language: ini

Templates
---------

Templates are used to generate the email body. There is three types of templates:

    - ``html``: HTML template
    - ``text``: Text template
    - ``string``: String template(just used in python code)

the variables in the template are {{ <variable-name> }} and they are the column name of contact list or the key values
in the input data dictionary of ``EmailSender.send`` method.

Two examples of template files are coming below:

**template.html**:

.. code-block:: html

    <html>
        <head></head>
        <body>
            <p>Hi {{ name }},</p>
            <p>This is a test email.</p>
            <p>Thanks,</p>
            <p>{{ sender }}</p>
        </body>
    </html>

**template.txt**:

.. code-block:: text

        Hi {{ name }},

        This is a test email.

        Thanks,

        {{ sender }}


Python usage
------------

Below is a Python script that demonstrates how to send a single email:

.. literalinclude:: ../../examples/base-usage.py
   :language: python


CLI Usage
---------

.. note::
   After :ref:`installation <installation>`, you can use the command line tool ``pyautomail`` to send emails.

.. toctree::
   :maxdepth: 2

   ./cli
   ./cli-best-practices
