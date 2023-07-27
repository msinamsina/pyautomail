# Automail: A Python pkg and command-line interface for Sending email to your contact list


<div style="text-align: center;">
<img  src='docs/_static/automail-logo.png'>
</div>

Welcome to the documentation for automail, a powerful Python package designed
for automated email sending, especially tailored for large scale operations
and Gmail automation. In today's fast-paced digital world, effective email
communication is a vital aspect of many businesses and projects.
However, manually sending individual emails or even managing bulk
email campaigns can be time-consuming and error-prone.


## Installation
```bash
pip install git+git@github.com:msinamsina/automail.git
```

## How to use in command-line interface
At first, you should register your email address and contact list
```bash
automail register <your-email-address> <Path-to-your-contact-list> [options]
```
Then you can send email to your contact list
```bash
automail start <process-id>
```
## How to use in python
```python
    from automail import EmailSender
    email_sender = EmailSender()
    email_sender.set_template('body.txt')
    data = {'name': 'Jon', 'age': 30}
    email_sender.send('msinamsina@gmail.com', 'sub1', data)
```

For more information, you can read the [documentation](https://automail.readthedocs.io/en/latest/)


## Old version (This script is deprecated)
The old version script is still available, and you can use it by following the below instruction

- sending empty message:
```bash
  python sending_gmail.py your-email@gmail.com ./contact.csv 
```
- sending simple message:
```bash
  python sending_gmail.py your-email@gmail.com ./contact.csv  --body body.txt 
```
- sending html message:
```bash
  python sending_gmail.py your-email@gmail.com ./contact.csv  --html html.html 
```
- sending one pdf file:
```bash
  python sending_gmail.py your-email@gmail.com ./contact.csv  --attachment document.pdf 
```
- sending custom pdf file:
```bash
  python sending_gmail.py your-email@gmail.com ./contact.csv  --cpdf
```

### For setting subject you have two options:
1- write subject in a txt file and use --> --subject_file sub.txt key

2- use --subject_txt key and write subject string directly

### add Custom data for contacts
1- adding columns with arbitrary names like 'data1' or 'name' and filling every row with related data

2- In the template file, you can use the word {column-name}  for the name of each column.
for example {data1} or {name}

### You can use -h or --help keys also
