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

parser = argparse.ArgumentParser()

parser.add_argument("email", help="enter you Gmail account")
parser.add_argument("contacts", help="path to csv file which contact emails are listed there")
parser.add_argument("--body", help="path to E-mail text file")
parser.add_argument("--html", help="path to E-mail Html file")
parser.add_argument("--attachment", help="path to pdf file that you want to attach to your E-mail")

arg=parser.parse_args()

sender_email = arg.email
receivers_email = []
with open(arg.contacts) as contactFile:
    for email in contactFile:
        receivers_email.append(email.split('\n')[0])

port = 465  # For SSL
password = getpass.getpass("Enter you email password  :") 

subject = "An email with attachment from Python"

message = MIMEMultipart("alternative")
message["Subject"] = subject
message["From"] = sender_email

if arg.body:
    with open(arg.body) as f:
        body = f.read()
    message.attach(MIMEText(body, "plain"))
    print(body)

if arg.html:
    with open(arg.html) as f:
        html = f.read()
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

for receiver in receivers_email:
    message["To"] = receiver    
    text = message.as_string()
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, text)
        time.sleep(10)
        print('message send to '+receiver)
