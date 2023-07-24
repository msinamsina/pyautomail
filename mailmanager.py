import argparse
import random


def registration(username, contacts, **args):
    print(f"ID:{random.randint(0,10)} => Registering user {username} with contacts {contacts}")


def start(lid, **args):
    print(f"ID:{lid} => Running the program")


def resume(pid, **args):
    print(f"ID: {pid} => Resume the program")


def parser():
    parser_obj = argparse.ArgumentParser(description='Mail Manager', prog="mailmanager")
    sud_parser = parser_obj.add_subparsers(dest='command')
    register_parser = sud_parser.add_parser('register', help='Register a new user')
    register_parser.add_argument('username', help='Username')
    register_parser.add_argument('contacts', help='Contacts')
    register_parser.add_argument('--template', help='Path to HTML or TXT Template')
    register_parser.add_argument('--subject', help='Subject of the email')
    register_parser.add_argument("--attachment", help="path to pdf file that you want to attach to your E-mail")
    register_parser.add_argument("--cpdf", action='store_true', help="custom pdf file that you want to attach to"
                                                                     " your E-mail", default=False)
    register_parser.add_argument("--pdf_dir", default='')
    register_parser.set_defaults(func=registration)

    start_parser = sud_parser.add_parser('start', help='Run the program')
    start_parser.add_argument('lid', help='list id')
    start_parser.set_defaults(func=start)

    resume_parser = sud_parser.add_parser('resume', help='Run the program')
    resume_parser.add_argument('pid', help='process id')
    resume_parser.set_defaults(func=resume)

    return parser_obj


if __name__ == '__main__':
    parser = parser()
    args_ = parser.parse_args()
    args_.func(**vars(args_))
