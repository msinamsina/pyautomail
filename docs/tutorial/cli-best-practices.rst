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


