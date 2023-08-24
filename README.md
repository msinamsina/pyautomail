# PyAutoMail: A Python package and command-line interface for automation sending email to your contact list


![pyautomail-image](./docs/_static/automail-logo.png)


Pyautomail, an incredibly powerful Python package meticulously crafted for the purpose of automated email delivery, catering especially to large-scale Email or Gmail automation. In today's fast-paced digital era, effective communication stands as a crucial cornerstone for numerous businesses and projects that heavily rely on email as their primary medium of interaction. Nonetheless, the manual handling of individual emails or the management of bulk email campaigns can prove to be both time-consuming and prone to errors.

Fear not, for pyautomail swoops in as the ultimate savior, offering a seamless and highly efficient solution for automating email communication. Be it the need to dispatch personalized emails to a vast audience, the execution of targeted email marketing campaigns, or the automation of repetitive email chores, this package serves as your ultimate go-to tool. With its user-friendly interface and an array of versatile features, pyautomail proves itself as a fitting choice for a wide range of applications, catering to startups, enterprises, professionals, and developers alike.

Revolutionize your email operations, whether it involves mass email distribution, streamlined Gmail tasks, or the quest for enhanced email communication proficiency - pyautomail is here to streamline your workflow, elevate your efficiency, and elevate productivity to soaring heights.


## Installation

### [PyPi](https://pypi.org/project/pyautomail/)
```bash
pip install pyautomail
```

### [Github](https://github.com/msinamsina/pyautomail.git)
```bash
pip install git+https://github.com/msinamsina/pyautomail.git
```

## How to use in command-line interface

1. At first, you should initialize project
    ```bash
    python -m pyautomail init
    ```
    
   After running this command, you will see a some questions. You should answer them.
    
   ```bash
   Where do you want to initialize the pyautomail project? [./pyautomail-workspace]
   What is your smtp server? [smtp.gmail.com]:
   What is your smtp port? [465]:
   ```
   
    **📘 Note:**   
    1. This command will create a folder with the project name in the path you specified. 
    If you don't specify the path, it will create ```automail-workspace```.  
    2. You can change the default smtp server by default it has been set on **Gmail Smtp Server**. 
    3. You also can set the port of **Smtm Server** (by default 465).
    4. Additionally, if you want to save you password in config file, you can use the ```-p``` or 
   ```--pasword``` switch.
    5. Moreover, if you want to initialize a test project, you can use ```-t``` or ```--test```. 
       ```bash
       $ pyhhon -m pyautomail init -t -p <your-password>
       ```

   > **[📙 Important]()**  
   > If directory already exists, it will be overwritten.
   
1. Then you should go to the project directory and register your contact list
    ```bash
    cd <your-project-name>
    python -m pyautomail register <Path-to-your-contact-list> [options]
   ```
   **📘 Note:**   
   For using a template, use ```--template``` switch. The template can be ```.txt``` or ```.html```
   Format.
   ```bash
   python -m pyautomail register contact-list.csv --template ./body.html
   ```
   **body.html:**
   ```html
   <h1> Hi {{ name }}, </h1>
   ```
   **contact-list.csv:**
   ```csv
   email,name,data1,cpdf
   contact1@gmail.com,contact1,ali,/path/to/pdf1
   contact2@gmail.com,contact2,mohammad,/path/to/pdf2
   contact3@gmail.com,contact3,soheila,/path/to/pdf3
   ```
   
1. Now you can start sending emails by running the following command
   ```bash
   python -m pyautomail start <process-id>
   ```
   
## How to use in python

```python
    from pyautomail import EmailSender
    email_sender = EmailSender()
    email_sender.set_template('body.txt')
    data = {'name': 'Jon', 'age': 30}
    email_sender.send('msinamsina@gmail.com', 'sub1', data)
```

## Documentation and Resources

For more comprehensive information about **PyAutoMail** and its capabilities, please explore our detailed [documentation](https://pyautomail.readthedocs.io/en/latest/).

- Get a brief overview and explore the features of PyAutoMail in the [Introduction](https://pyautomail.readthedocs.io/en/latest/introduction.html) section.
- If you're new to PyAutoMail, follow our [Getting Started](https://pyautomail.readthedocs.io/en/latest/getting-started.html) guide to kickstart your email automation journey.
- For a quick reference, you can check out the [API Reference](https://pyautomail.readthedocs.io/en/latest/api/index.html) section.
- To gain deeper insights into PyAutoMail and learn best practices, dive into our informative [Tutorial](https://pyautomail.readthedocs.io/en/latest/tutorial/index.html) section.

By exploring these resources, you'll harness the full potential of PyAutoMail and make the most out of its powerful email automation capabilities.

---

## Contribution and Support

We welcome contributions from the community to enhance **PyAutoMail** and make it even more robust. If you're interested in contributing, here's how you can get involved:

1. **Bug Reports and Feature Requests**: If you come across any issues or have ideas for new features, please [open an issue](https://github.com/msinamsina/automail/issues) on our GitHub repository. We appreciate detailed bug reports with steps to reproduce the problem and clear feature requests with use cases.

2. **Pull Requests**: If you want to contribute code to PyAutoMail, you can do so by submitting a pull request. Please ensure that your code adheres to the existing code style, and include relevant tests to maintain code quality.

3. **Documentation**: Improving the documentation is always valuable. If you find any inconsistencies or areas that need clarification, feel free to submit documentation updates via pull requests.

4. **Spread the Word**: If you find PyAutoMail useful, help us spread the word by sharing it with your peers and on social media platforms.
