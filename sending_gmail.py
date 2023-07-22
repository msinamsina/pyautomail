# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:09:32 2020

@author: Mohammad sina Allahkaram
"""

import argparse
import getpass 
import pandas as pd
import os
from emailsender import EmailSender
import logging
import sys


logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s')
handler1 = logging.StreamHandler(sys.stdout)
handler1.setFormatter(formatter)
handler2 = logging.FileHandler('emailsender.log')
handler2.setFormatter(formatter)
logger.addHandler(handler1)
logger.addHandler(handler2)



def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("email", help="enter you Gmail account")
    parser.add_argument("contacts", help="path to csv file which contact emails are listed there")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--subject_txt", help="string of subject")
    group.add_argument("--subject_file", help="text file that 'subject' written there")
    parser.add_argument("--body", help="path to E-mail text file")
    parser.add_argument("--html", help="path to E-mail Html file")
    parser.add_argument("--attachment", help="path to pdf file that you want to attach to your E-mail")
    parser.add_argument("--cpdf", action='store_true', help="custom pdf file that you want to attach to your E-mail",
                        default=False)
    parser.add_argument("--pdf_dir", default='')
    parser.add_argument("--template", help="path to template file")

    return parser.parse_args()

logger.info("Reading arguments...")
arg = arg_parser()

sender_email = arg.email
contact_df = pd.read_csv(arg.contacts)
port = 465  # For SSL
#
password = "1234"#getpass.getpass("Enter you email password  :")

# Create a secure SSL context
logger.info("Creating EmailSender obj...")
sender = EmailSender(cfg="config.cfg", is_test=True)


subject=''
if arg.subject_txt:
    subject =  arg.subject_txt
elif arg.subject_file:
    with open(arg.subject_file) as f:
        subject = f.read()

logger.info("Subject: {}".format(subject))


for i in contact_df.iterrows():

    if arg.body:
        sender.set_template(arg.body)
    if arg.html:
        sender.set_template(arg.html)
    if arg.template:
        sender.set_template(arg.template)

    filename = None
    if arg.attachment:
        filename = arg.attachment

    if arg.cpdf:
        filename = os.path.join(arg.pdf_dir, str(i[1]['cpdf']) + '.pdf')

    data = {}
    for item in i[1].items():
        data[item[0]] = item[1]

    print(data)

    sender.send(i[1]['email'], subject, data, filename)