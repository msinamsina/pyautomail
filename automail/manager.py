import argparse
from automail.storage import Record, Process, session
import datetime
import pandas as pd
import os
import logging
import sys
import getpass
from automail.emailsender import EmailSender
import time


# TODO: add a command to delete a process
# TODO: add a command to delete a record
# TODO: table for process in process_list function
# TODO: table for record
# TODO: add a command to edit a process
# TODO: add a command to edit a record
# TODO: create a logger pkg
def init_logger():
    logger_obj = logging.getLogger('manager')
    logger_obj.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s')
    handler1 = logging.StreamHandler(sys.stdout)
    handler1.setFormatter(formatter)
    handler2 = logging.FileHandler('../emailsender.log')
    handler2.setFormatter(formatter)
    logger_obj.addHandler(handler1)
    logger_obj.addHandler(handler2)
    return logger_obj


def registration(username, contacts, name, cpdf, attachment, pdf_dir, **args):
    process = Process(title=name, subject=args['subject'], sender=username,
                      temp_file=args['template'], release_date=datetime.datetime.date(datetime.datetime.now()))
    session.add(process)
    session.commit()

    print(f"ID:{process.id} => Registering user {username} with contacts {contacts}")
    contact_df = pd.read_csv(contacts)
    for index, row in contact_df.iterrows():
        filename = None
        if attachment:
            filename = attachment

        if cpdf:
            filename = os.path.join(pdf_dir, str(row['cpdf']) + '.pdf')
        record = Record(receiver=row['email'], data=row.to_json(), process_id=process.id, attachment_path=filename)
        session.add(record)
        session.commit()
        print(f"ID:{record.id} => Registering record for {row['email']}")


def run(pid, resume=True):
    logger = init_logger()
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
    run(pid, resume=False)


def stop(pid, **args):
    process = session.query(Process).filter(Process.id == pid).first()
    if process.status == "in progress":
        process.status = "paused"
        session.commit()
        print(f"ID: {pid} => Pausing the program")
    else:
        print(f"ID: {pid} => Program is not running")


def resume_process(pid, **args):
    run(pid, resume=True)


def process_list(pid=None, **kwargs):
    if pid is None:
        processes = session.query(Process).all()
    else:
        processes = session.query(Process).filter(Process.id == pid).all()

    for process in processes:
        print(process.id, process.title, process.status,
              len(session.query(Record).filter(Record.process_id == process.id, Record.status == "unsent").all()),
              len(session.query(Record).filter(Record.process_id == process.id, Record.status == "sent").all()))


def parser():
    parser_obj = argparse.ArgumentParser(description='Mail Manager', prog="mailmanager")
    sud_parser = parser_obj.add_subparsers(dest='command')
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
    list_parser.set_defaults(func=process_list)
    return parser_obj


def main():
    parser_ = parser()
    args_ = parser_.parse_args()
    args_.func(**vars(args_))


if __name__ == '__main__':
    main()
