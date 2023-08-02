"""This module is responsible for managing the automail pkg.
It has below commands:

1. register: register a new contact list and a new process this command will get below arguments:
    - username: the email address of the sender
    - contacts: the path to the csv file which contains the contacts
    - name(optional): an arbitrary name for the process
    - subject(optional): the subject of the email
    - template(optional): the path to the template file
    - cpdf(optional): this is a flag that if it is set, the pdf file will be customized for each contact based on the \
    path to the pdf file which is in the contacts csv file in the column 'cpdf'
    - attachment(optional): the path to the attachment file if you want to attach a same file to all emails
    - pdf_dir(optional): the path to the directory which contains the pdf files if you want to use cpdf flag
2. start: this command will start a process and get the process id as argument you can find the process id in the list\
 of processes by: `automail list` command
3. list: list processes
4. stop: this command will stop one specific process by process id
5. resume: this command will resume one specific process by process id
"""
import argparse
from automail.storage import Record, Process, get_session, create_tables
import datetime
import pandas as pd
import os
import getpass
from automail import EmailSender
from automail.utils import init_logger
import time
# TODO: add a command to delete a process
# TODO: add a command to delete a record
# TODO: table for process in process_list function
# TODO: table for record
# TODO: add a command to edit a process
# TODO: add a command to edit a record
# TODO: create a logger pkg

__all__ = ['registration', 'start', 'stop', 'resume_process', 'list_processes', 'run']


def init(*args, **kwargs):
    project_name = input('Enter the name of your project: ')
    path = input('Enter the path to your project (default is current directory): ')
    if path == '':
        path = os.getcwd()
    else:
        path = os.path.abspath(path)
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    session, engin = get_session()
    create_tables(engin)

    session.close()
    engin.dispose()


def registration(username, contacts, name="", cpdf=False, attachment="", pdf_dir="", **args):
    """This function will register a new process and a new contact list


    Parameters
    ----------
    username : str
        the email address of the sender
    contacts : str
        the path to the csv file which contains the contacts
    name : str
        an arbitrary name for the process
    cpdf : bool
        this is a flag that if it is set, the pdf file will be customized for each contact based on the \
        path to the pdf file which is in the contacts csv file in the column 'cpdf'
    attachment : str
        the path to the attachment file if you want to attach a same file to all emails
    pdf_dir : str
        the path to the directory which contains the pdf files if you want to use cpdf flag
    args : dict
        the other arguments which are passed to the function

    Returns
    -------
    None

    Notes
    -----
    This function will register a new process plus records for each contact in the contacts csv file.

    """
    from automail.storage import register_new_process

    register_new_process(title=name, email=username, contact_list=contacts, custom_pdf=cpdf, attachment=attachment,
                         custom_pdf_dir=pdf_dir, subject=args.get('subject', ""), template=args.get('template', ""))
    print("Process registered successfully!")
    print("You can start the process with 'automail start <process_id>' command")


def run(pid, resume=True):
    """
    This function will run a process with a specific id

    Parameters
    ----------
    pid : int
        the process id
    resume : bool
        if True, the program will resume the process if it is paused, otherwise it prints a warning message and \
        return without doing anything
    """
    session, engin = get_session()
    create_tables(engin)

    session.close()
    engin.dispose()
    logger = init_logger('manager')
    logger.info("Reading arguments...")
    process = session.query(Process).filter(Process.id == pid).first()
    if not process:
        logger.error(f"ID:{pid} => Process not found. You can see all processes with 'mailmanager list' command")
        return
    sender_email = process.sender
    subject = process.subject
    temp_file = process.temp_file
    if resume:
        if process.status != "paused":
            print(f"ID:{pid} => Program is already {process.status}")
            return
        contacts = session.query(Record).filter(Record.process_id == pid, Record.status == "unsent").all()
    else:
        if process.status in ["paused", "in progress", 'finished']:
            logger.warning(f"ID:{pid} => Program is already {process.status}")
            print(f"ID:{pid} => Program is already {process.status}")
            print(f"You can resume the program with 'mailmanager resume {pid}' command")
            print(f"You can see all processes with 'mailmanager list' command")
            while True:
                check = input(f"Are you sure you want to sent all email again? (y/n)")
                if check == "n":
                    return
                elif check == "y":
                    break
                else:
                    print("Please enter y or n!")
        contacts = session.query(Record).filter(Record.process_id == pid).all()

    password = getpass.getpass("Enter you email password  :")

    # Create a secure SSL context
    logger.info("Creating EmailSender obj...")
    sender = EmailSender(cfg="config.cfg", user=sender_email, password=password)
    if temp_file:
        sender.set_template(temp_file)

    process.status = "in progress"
    session.commit()

    pause = False
    for contact in contacts:
        process = session.query(Process).filter(Process.id == pid).first()
        if process.status == "paused":
            logger.info(f"ID:{pid} => Pausing the program")
            pause = True
            break
        logger.info(f"Sending email to {contact.receiver}")
        sender.send(contact.receiver, subject, contact.data)
        contact.status = "sent"
        session.commit()
        logger.info(f"ID:{contact.id} => Email sent to {contact.receiver}")
        time.sleep(10)

    if not pause:
        process.status = "finished"
        session.commit()
        logger.info(f"ID:{pid} => Program finished successfully")


def start(pid, **args):
    """This function will start a process with a specific id"""
    run(pid, resume=False)


def stop(pid, **args):
    """This function will stop a process with a specific id"""
    session, engin = get_session()
    create_tables(engin)

    session.close()
    engin.dispose()
    process = session.query(Process).filter(Process.id == pid).first()
    if process.status == "in progress":
        process.status = "paused"
        session.commit()
        print(f"ID: {pid} => Pausing the program")
    else:
        print(f"ID: {pid} => Program is not running")


def resume_process(pid, **args):
    """This function will resume a process with a specific id"""
    run(pid, resume=True)


def list_processes(pid=None, **kwargs):
    """This function will print the list of all processes or a specific process with a specific id

    Parameters
    ----------
    pid : int
        the process id if you want to see the information of a specific process or None if you want to see the \
        information of all processes
    """
    session, engin = get_session()
    create_tables(engin)

    session.close()
    engin.dispose()
    if pid is None:
        processes = session.query(Process).all()
    else:
        processes = session.query(Process).filter(Process.id == pid).all()

    for process in processes:
        print(process.id, process.title, process.status,
              len(session.query(Record).filter(Record.process_id == process.id, Record.status == "unsent").all()),
              len(session.query(Record).filter(Record.process_id == process.id, Record.status == "sent").all()))


def _parser():
    parser_obj = argparse.ArgumentParser(description='Automail', prog="automail")
    sud_parser = parser_obj.add_subparsers(dest='command')

    init_parser = sud_parser.add_parser('init', help='Initialize the database')
    init_parser.set_defaults(func=init)

    register_parser = sud_parser.add_parser('register', help='Register a new user')
    register_parser.add_argument('username', help='Username')
    register_parser.add_argument('contacts', help='Contacts')
    register_parser.add_argument('--name', help='A name')
    register_parser.add_argument('--template', help='Path to HTML or TXT Template')
    register_parser.add_argument('--subject', help='Subject of the email')
    register_parser.add_argument("--attachment", help="path to pdf file that you want to attach to your E-mail")
    register_parser.add_argument("--cpdf", action='store_true', help="custom pdf file that you want to attach to"
                                                                     " your E-mail", default=False)
    register_parser.add_argument("--pdf_dir", default='')
    register_parser.set_defaults(func=registration)

    start_parser = sud_parser.add_parser('start', help='Start a process that is registered by id')
    start_parser.add_argument('pid', help='process id')
    start_parser.set_defaults(func=start)

    stop_parser = sud_parser.add_parser('stop', help='Stop a process that is running by id')
    stop_parser.add_argument('pid', help='process id')
    stop_parser.set_defaults(func=stop)

    resume_parser = sud_parser.add_parser('resume', help='Resume a process that is paused by id')
    resume_parser.add_argument('pid', help='process id')
    resume_parser.set_defaults(func=resume_process)

    list_parser = sud_parser.add_parser('list', help='List processes (all or a specific proces  by id')
    list_parser.add_argument('--pid', help='process id', default=None, required=False)
    list_parser.set_defaults(func=list_processes)

    return parser_obj


def main(args=None):
    parser_ = _parser()
    args_ = parser_.parse_args(args)
    args_.func(**vars(args_))


if __name__ == '__main__':
    main()
