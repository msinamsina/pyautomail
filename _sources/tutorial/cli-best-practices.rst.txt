CLI Best Practices
==================

This part of document describes the best practices for using the Pyautomail CLI. It is intended to be a living document,
and will be updated as new best practices are discovered.

Before anything else, It's needed to discuss the basic concepts of Pyautomail CLI. The Pyautomail CLI needs three main
steps to send emails to the recipients.

1. For working with pyautomail at first a project should be initialized. This step is done by
:ref:`pyautomail init <init command>` command. This command creates a project directory with the name of the project
and a config file named `config.cfg` in the project directory. The config file contains the project settings and user
can change the settings by editing the config file.
After initializing the project, the other steps must be done in the project directory.

2. The second step is to register a **Process**. A process has a set of common information that is needed to send
emails to recipients. The common information includes the email **template**, the email **subject**, the email
**attachments** and the email **sender**. Processes also have **Records**. Every record contain the **recipients**
information like **email addresses** and related **datas** of every recipient.

3. In the last step of the user can **start**, **stop**, **resume**, **delete** processes which is registered in the
project. The user can also **list** the processes and see the status of them.


Initializing Project
---------------------
At first you need init the project and go inside of project directory.

.. code-block:: bash

    pyautomail init -db PAM-workspace -ss smtp.gmail.com -sp 465 -e example@gmail.com
    cd PAM-workspace


Example 1: Sending a common Email to all recipients
---------------------------------------------------
For sending a common email to all recipients, you need create a template file anywhere you want. We recommend to create
``.html`` format. There is no limitation for the template file name. For example we create a template file named
``template.html`` . The template file can contain any information you want. For example we create a template file
with the following content:

.. code-block:: html

    <html>
        <body>
            <h1>Hi everyone!</h1>
            <p>This is a test email.</p>
        </body>
    </html>

After creating the template file, you need to register a process, but before that you need to prepare a ``.csv`` file
that contains the recipients information. The ``.csv`` file must contain a column named which is **EXACTLY** ``email``
that contains the email addresses of the recipients. For example we create a ``.csv`` file named ``recipients.csv``
with the following:

.. code-block:: text

    email,
    receiver1@gmail.com
    receiver2@gmail.com
    receiver2@gmail.com
    other@email.co
    ...

After creating the ``.csv`` file, you can register a process with the following command:

.. code-block:: bash

    pyautomail register  recipients.csv -t template.html -s "Test Email" -T "list1" -e sender@gmail.com

This command registers a process with the name of ``recipients.csv`` and the template file ``template.html`` and the
subject of ``Test Email`` and the sender email address of ``sender@gmail.com``. The process is registered with the
name of ``list1``. As you sow, the sender email address can be different from the email address that you used for
initializing the project but you can use the same one. After registering the process, the following output will be
shown:

.. code-block:: bash

    ID: 1 => Registering Process sender@gmail.com with contacts list1\recipients.csv
    ID:1 => Registering record for receiver1@gmail.com
    ID:2 => Registering record for receiver2@gmail.com
    ID:3 => Registering record for receiver2@gmail.com
    ID:4 => Registering record for other@email.co
    ...

As you can see the process is registered with the ID of ``1`` and the records are registered with the ID of ``2``,
``3``, ``4`` and so on. The ID of the process is used for starting, stopping, resuming and deleting the process.

After registering the process, now you are ready to start the process and send emails to the recipients. You can start
the process with the following command:

.. code-block:: bash

    pyautomail start 1

After running this command the following question will be asked:

.. code-block:: text

    Do you want to use the initial password for sender@gmail.com? [Y/n]:

And you should enter ``n`` then enter your password.

.. warning::
    It is recommended to don't save you password in config file, because it is not secure.

After entering the password, if you email address and password are correct, the process will be started, otherwise the
following output will be shown:

.. code-block:: bash

    [2023-08-25 14:27:36 - INFO (EmailSender) ] : Initializing EmailSender...
    [2023-08-25 14:27:36 - INFO (EmailSender) ] : Connecting to SMTP server...
    [2023-08-25 14:27:36 - INFO (EmailSender) ] : Connected to SMTP server.
    [2023-08-25 14:27:36 - INFO (EmailSender) ] : Logging in to user account: sender@gmail.com...
    [2023-08-25 14:27:37 - ERROR (EmailSender) ] : Authentication ERROR: Username and Password not accepted. Please check username and password and try again
    [2023-08-25 14:27:37 - INFO (EmailSender) ] : Closing connection to SMTP server...
    [2023-08-25 14:27:37 - INFO (EmailSender) ] : Connection closed.

