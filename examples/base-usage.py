from pyautomail import EmailSender

# Creating a sender object
sender = EmailSender(cfg="./assets/config.cfg")
# Set the template
sender.set_template('./templates/body.txt')
# Custom data
data = {'name': 'Jon', 'age': 30}
# Send the email to 'contact1@gmail.com' with Subject 'sub1' and custom date
sender.send('contact1@gmail.com', 'sub1', data)
# Repeat the above steps but using a '.html' template
data = {'name': 'Mike', 'age': 30}
sender.set_template('./templates/html.html')
sender.send('contact2@gmail.com', 'sub2', data)
# plain_temp
data = {'name': 'Mike', 'age': 30}
sender.set_template(plain_temp="{{ name }}-{{ age }}")
sender.send('contact2@gmail.com', 'sub2', data)
