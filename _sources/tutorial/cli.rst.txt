Command-line interface (CLI) tool
=================================

Pyautomail has prepared an easy to use CLI tool which gather several useful command for creating and editing lists of
your contacts emails, templates and so on.

Pyautomail CLI can be used by following commands:

.. code-block::

    pyautomail <command>

It support the following commands:

    - :ref:`init <init command>`
    - :ref:`register <register command>`
    - :ref:`list <list command>`
    - :ref:`list-records <list-records command>`
    - :ref:`start <start command>`
    - :ref:`stop <stop command>`
    - :ref:`resume <resume command>`
    - :ref:`delete-process <delete-process command>`
    - :ref:`delete-record <stop command>`

init command
------------

Before anything else, pyautomail project should be initialized. This is done by the following command:

.. code-block:: bash

    pyautomail init [options]

This command has the following options:

    - ``--db-path`` or ``-db``: This option is used for setting the name of project and refers to
      the path of database directory.
    - ``--smtp-serve`` or ``-ss``: This option is used for setting the smtp host of your project.
    - ``--smtp-port`` or ``-sp``: This option is used for setting the smtp port of your project.
    - ``--email`` or ``-e``: This option is used for setting the default email address of your project.
    - ``--password`` or ``-p``: This option is used for setting the default email password of your project.
    - ``--test`` or ``-t``: This option sets the testing mode and in this mode no email will be sent.
    - ``--help``: This option is used for showing the help message.


If the ``init`` command is run without necessary options, some questions will be asked that help client
to initialize the project. The questions are as follows:

1. If ``--db-path`` or ``-db`` option is not set, the following question will be asked:

    .. code-block:: text

        Where do you want to initialize the automail project? [./automail-workspace]:

    The path or name of the directory in which the project should be initialized must be entered after this question.

    .. note::
        The directory should be empty or be an old pyautomail project and if that directory doesn't exist it will be
        created after ``init`` command.

2. If ``--smtp-serve``, ``-ss``, ``--smtp-port`` or ``-sp`` options is not set, the following questions will be asked:

    .. code-block:: text

        What is your smtp server? [smtp.gmail.com]:
        What is your smtp port? [465]:

    These two questions are about smtp server setting. The smtp host and port should be entered.
    (by default the pyautomail is set on GMAIL server).

    .. note::
        For more information about smtp server please see the following links:

        - https://sendgrid.com/blog/what-is-an-smtp-server/
        - https://blog.cpanel.com/setting-up-and-troubleshooting-smtp-in-cpanel/

3. If ``--email`` or ``-e`` option is not set, the following question will be asked:

    .. code-block:: text

        Enter a default email address? [<your-email>]:

    The answer of this question will set a default email address for your project.

    .. note::
        This email address can be used as the default sender email address but you can set another email
        address for every list of your contacts. For more information please
        see :ref:`register <register command>` command.


4. If ``--password`` or ``-p`` option is not set, the following question will be asked:

    .. code-block:: text

        If you want to save the password of default email please enter your password
        otherwise press enter to continue? [None]:

    This question is about default email password. If the password is entered, it will be saved in the config file.
    Otherwise, if it's leaved empty the password should be entered every time you want to :ref:`start <start command>`
    a process.

    .. warning::
        If you want to save your password in the config file, you should know that it will be saved in plain
        text format. So, it is not recommended to save your password in the config file.

When the pyautomail project initialization process is done, a new directory with the name of your project will be
created which the following files exist on it:

.. code-block:: text

    <project-name>
        |_ config.cfg
        |_ mail.db

The config.cfg file contains the configuration of your project and the mail.db file is a sqlite database which is stored
the processes ans records of your project.

**config.cfg**:

.. literalinclude::
    ../../examples/assets/config.cfg
    :language: text


User can edit this file manually. But, it is recommended to use the ``init`` command for editing this file.


.. important::
    All the other command must be run from the inside of the project folder. For more information see
    :doc:`cli best practices <./cli-best-practices>`


register command
----------------

This command is used to register a new list of contacts. You can register a new list of contacts by the following
command:

.. code-block:: bash

    pyautomail register <path/to/contacts/file> [options]

The ``<path/to/contacts/file>`` is the path of your contacts file. The contacts file should be a ``.csv`` file and
must have a column with the name of ``email``. Every row of this column should be a valid email address.

Other columns of the contacts file are optional and you can add as many columns as you want. The name of the columns
will be used as the name of the variables in the template file. For example, if you have a column with the name of
``name``, you can use the ``{{ name }}`` in your template file.

Additionally, if you want to attach a custom file to every email the ``.csv`` file should have a column with name of
``cpdf``, every row of this column should be the path of your file.

There is an example of the contact-list.csv:

.. literalinclude:: ../../examples/assets/contact.csv
   :language: text

The register command also has some options which are as follows:

    - ``--email`` or ``-e``: This is used for setting the sender email address of the list.
    - ``--title`` or ``-T``: This is used to set a title for the list. The title should be unique.
    - ``--template`` or ``-t``: The path of the template file.
    - ``--subject`` or ``-s``: The subject of the email.
    - ``--custom-pdf`` or ``-CA``: This is a switch option and if is set, the custom pdf file will be attached to
      every email. based on the ``cpdf`` column of the contacts file.
    - ``attachment`` or ``-a``: The path of the attachment file. This file will be attached to every email.
    - ``--custom-pdf-dir`` or ``-cpd``: The path of the directory that contains the custom pdf files. This option
      will be used if the ``--custom-pdf`` option is set.
    - ``--help``: This is used for showing the help message.

If the ``register`` command is run without any option, the pyautomail will ask some questions. The questions are as
follows:

    .. code-block:: text

        What is your email address? [default(see config.cfg)]:
        What is the title of your contact list? [Contact List]:
        What is the subject of your email? [None]:
        Do you want to use template? [y/N]:

After registering a new list of contacts, a new directory with the name of your list will be created in the
``<project-name>/<title>`` directory and returns the id of the list.

    .. code-block:: text

        ID: 1 => Registering Process <your-email> with contacts Contact List\contact.csv

Additionally, all registered lists can be seen by the :ref:`list <list command>` command.


start command
-------------

This command is used to start a process. You can start a process by the following command:

.. code-block:: bash

    pyautomail start <process-id>

list command
------------

This command is used to show all registered lists. You can see all registered lists by the following command:

.. code-block:: bash

    pyautomail list

list-records command
--------------------

This command is used to show all records of a list. You can see all records of a list by the following command:

.. code-block:: bash

    pyautomail list-records <process-id>

stop command
------------

This command is used to stop a process. You can stop a process by the following command:

.. code-block:: bash

    pyautomail stop <process-id>


resume command
--------------

This command is used to resume a process. You can resume a process by the following command:

.. code-block:: bash

    pyautomail resume <process-id>


delete-process command
----------------------
This command is used to delete a list. You can delete a list by the following command:

.. code-block:: bash

    pyautomail delete-process <process-id>


.. warning::
    This command will delete all data of the list. So, be careful when you want to use this command.

delete-record command
---------------------

This command is used to delete a record of a list. You can delete a record by the following command:

.. code-block:: bash

    pyautomail delete-record <process-id> <record-id>


.. warning::
    This command will delete the record of the list. So, be careful when you want to use this command.