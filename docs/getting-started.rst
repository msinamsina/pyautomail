Quickstart with automail
=============================

Welcome to automail! This guide will help you get up and running with the automated
email sending Python package in no time.

.. note::
    This guide assumes that you have some basic knowledge of Python and the command line.
    If you are new to Python, you can check out the official Python tutorial
    `here <https://docs.python.org/3/tutorial/index.html>`_.
    If you are new to the command line, you can check out this
    `tutorial <https://www.codecademy.com/learn/learn-the-command-line>`_.

Before you begin, make sure you have Python installed on your system, preferably
Python 3.9 or higher.

.. important::
    If you are not a Python developer, don't worry! You don't need to write any
    Python code to use automail. You can use the command-line interface (CLI) tool
    to send emails without writing any code. Please refer to the
    :ref:`automail command-line interface (CLI) tool <cli>`

    **Additionally a user interface will be provided in the future.**


Installation
------------

To install automail, you can use pip and git to install the package directly from GitHub:

.. code-block:: bash

    $ pip install git+https://github.com/msinamsina/automail.git


This will download and install the latest version of automail along with its dependencies.

Alternatively, you can clone the repository and install the package from source:

.. code-block:: bash

    $ git clone git@github.com:msinamsina/automail.git
    $ cd automail
    $ pip install .

How to Use
----------
There are two ways to use automail to send emails. You can either use the most powerful
command-line interface (CLI) tool without writing any Python code, or you can use the
Python package in your custom scripts. We'll cover a quick overview of both of these
options in this guide. For more details, please refer to :doc:`the Tutorial section <tutorial/index>`
and the :doc:`API reference <api/index>`.

.. _cli:

1. Automail command-line interface (CLI) tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you install automail, you will also get a command-line interface (CLI) tool called `automail`.
This tool can be used to send emails from the command line, without writing any Python code.
So if you want to send a quick email without writing a script, you can use the CLI tool.

To use the CLI tool, you will need to provide your contact list in a CSV file.
The CSV file should contain the following columns: `name`, `email` and other
columns can be added as contact information which will be used in the email template.

Here's an example of a CSV file containing a list of contacts:

.. code-block:: bash

    name,email,custom_data1,custom_data2
    John Doe,JohnDoe@gmail.com,John_data1,John_data2
    Jane Doe,JaneDoe@gmail.com,Jane_data1,Jane_data2


To send emails using the CLI tool, you can run the following command:

#. At first you should register a process

    - The process contains the email template and the contact list data and some other configurations.
    - You can register a process by running the following command:

        .. code-block:: bash

            $ automail register youremail@email.com\
            contacts.csv\
            --template template.html\
            --subject "Hello from automail!"

    - This command will register a process with the given email, contacts and template and give you a process id.
    - You can see all the registered processes by running the following command:

            .. code-block:: bash

                $ automail list

#. Now you can start a process by running the following command:

    .. code-block:: bash

        $ automail start <process_id>

    - This command will start the process with the given id and send the emails.
    - You also can stop a process by running the following command in another terminal:

            .. code-block:: bash

                $ automail stop <process_id>
    - And you can resume a stopped process by running the following command:

            .. code-block:: bash

                $ automail resume <process_id>

2. Writing your own python script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to automate your email sending process, you can also use the Python package in your custom scripts.
This will give you more flexibility and control over the email sending process.
You can use the Python package to send emails to multiple recipients, use custom email templates,
and customize other settings according to your needs.

There is an example script in the following:

.. code-block:: python

    from automail import EmailSender

    # Initialize automail with your email credentials and configurations
    automailer = EmailSender(user="your-email", password="your-password")

    # Send a single email
    automailer.set_template('body.txt')
    data = {'name': 'Jon', 'age': 30}
    automailer.send('dest-email', 'sub1', data)



Configuration
-------------

Before you start sending emails, you'll need to set up some configurations for automail.
This includes providing your email credentials, choosing the email service provider (e.g., Gmail),
and customizing other settings according to your needs.


Sending Emails with your custom script
--------------------------------------

You can also use automail in your custom Python scripts to send emails.
Here's a basic example of sending an email to a single recipient:

.. code-block:: python

    from automail import EmailSender

    # Initialize automail with your email credentials and configurations
    automailer = EmailSender(email='your_email@gmail.com', password='your_email_password')

    # Send a single email
    sender.set_template('body.txt')
    data = {'name': 'Jon', 'age': 30}
    sender.send('msinamsina@gmail.com', 'sub1', data)



For more advanced usage, such as sending emails to multiple recipients or using custom email templates,
please refer to the relevant sections in the documentation.

Conclusion
----------

You've completed the getting started guide for automail!
You should now be ready to automate your email communication with ease.
Feel free to explore the extensive documentation for more features, examples, and best practices.

Happy automailing!

**Keywords**: automail, Getting Started, Installation, Python Package, Automated Email Sending, Email Configuration, Email Credentials, Gmail Integration, SMTP Server, Custom Email Templates, Send Email.