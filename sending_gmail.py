# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:09:32 2020

@author: Mohammad sina Allahkaram
"""
import smtplib, ssl
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import getpass 
import pandas as pd


def replace_data(data, string):
    for i in data.items():
        print(i)
        string = string.replace('${}$'.format(i[0]), i[1])
    return string


parser = argparse.ArgumentParser()

parser.add_argument("email", help="enter you Gmail account")
parser.add_argument("contacts", help="path to csv file which contact emails are listed there")
group = parser.add_mutually_exclusive_group()
group.add_argument("--subject_txt", help="string of subject")
group.add_argument("--subject_file", help="text file that 'subject' written there")
parser.add_argument("--body", help="path to E-mail text file")
parser.add_argument("--html", help="path to E-mail Html file")
parser.add_argument("--attachment", help="path to pdf file that you want to attach to your E-mail")
parser.add_argument("--cpdf", action='store_true', help="custom pdf file that you want to attach to your E-mail", default=False)

arg=parser.parse_args()

sender_email = arg.email
receivers_email = []

contact_df = pd.read_csv(arg.contacts)


port = 465  # For SSL
password = getpass.getpass("Enter you email password  :") 

subject=''
if arg.subject_txt:
    subject =  arg.subject_txt
elif arg.subject_file:
    with open(arg.subject_file) as f:
        subject = f.read()


for i in contact_df.iterrows():
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email

    print(i[1]['name'])
# for receiver in receivers_email:
    if arg.body:
        with open(arg.body) as f:
            body = f.read()
            body = replace_data(i[1], body)
        message.attach(MIMEText(body, "plain"))
        print(body)
    if arg.html:
        with open(arg.html) as f:
            html = f.read()
            html = replace_data(i[1], html)
        message.attach(MIMEText(html, "html"))
        print(html)

    if arg.attachment:
        filename = arg.attachment

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)

    if arg.cpdf:
        filename = str(i[1]['cpdf'])

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)


    message["To"] = i[1]['email']
    text = message.as_string()
    
    # Create a secure SSL context
    #context = ssl.create_default_context()
    # ToDo : add smtp server and port as input args
    with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, i[1]['email'], text)
        time.sleep(10)
        print('message send to '+i[1]['email'])
