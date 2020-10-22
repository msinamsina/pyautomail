# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 14:09:32 2020

@author: 98936
"""
import smtplib, ssl
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




subject = "An email with attachment from Python"



port = 465  # For SSL
password = "your password"
gmail="your@gmail.com"


sender_email = gmail
receivers_email = []

receivers_email.append("contact1@gmail.com")
receivers_email.append("contact2@gmail.com")
receivers_email.append("contact3@gmail.com")


message = MIMEMultipart()



body = "This is an email with attachment sent from Python"

html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""


message.attach(MIMEText(body, "plain"))

message.attach(MIMEText(html, "html"))

filename = "document.pdf"  # In same directory as script

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
text = message.as_string()

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(gmail, password)
    # TODO: Send email here
    server.sendmail(sender_email, receivers_email[0], text)
    time.sleep(10)
    print('message send to '+receivers_email[0])
