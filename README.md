# PyAutoMail: A Python package and command-line interface for automation sending email to your contact list


<p align="center" width="100%">
    <img  width="80%" src="https://github.com/msinamsina/automail/blob/main/docs/_static/automail-logo.png?raw=true" >
</p>


Pyautomail, an incredibly powerful Python package meticulously crafted for the purpose of automated email delivery, catering especially to large-scale Email or Gmail automation. In today's fast-paced digital era, effective communication stands as a crucial cornerstone for numerous businesses and projects that heavily rely on email as their primary medium of interaction. Nonetheless, the manual handling of individual emails or the management of bulk email campaigns can prove to be both time-consuming and prone to errors.

Fear not, for pyautomail swoops in as the ultimate savior, offering a seamless and highly efficient solution for automating email communication. Be it the need to dispatch personalized emails to a vast audience, the execution of targeted email marketing campaigns, or the automation of repetitive email chores, this package serves as your ultimate go-to tool. With its user-friendly interface and an array of versatile features, pyautomail proves itself as a fitting choice for a wide range of applications, catering to startups, enterprises, professionals, and developers alike.

Revolutionize your email operations, whether it involves mass email distribution, streamlined Gmail tasks, or the quest for enhanced email communication proficiency - pyautomail is here to streamline your workflow, elevate your efficiency, and elevate productivity to soaring heights.


## Installation

### [PyPi](https://pypi.org/project/pyautomail/)
```bash
pip install pyautomail
```

### Github
```bash
pip install git+https://github.com/msinamsina/automail.git
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

### Documentation and Resources

For more comprehensive information about **PyAutoMail** and its capabilities, please explore our detailed [documentation](https://automail.readthedocs.io/en/latest/).

- Get a brief overview and explore the features of PyAutoMail in the [Introduction](https://automail.readthedocs.io/en/latest/introduction.html) section.
- If you're new to PyAutoMail, follow our [Getting Started](https://automail.readthedocs.io/en/latest/getting-started.html) guide to kickstart your email automation journey.
- For a quick reference, you can check out the [API Reference](https://automail.readthedocs.io/en/latest/api/index.html) section.
- To gain deeper insights into PyAutoMail and learn best practices, dive into our informative [Tutorial](https://automail.readthedocs.io/en/latest/tutorial/index.html) section.

By exploring these resources, you'll harness the full potential of PyAutoMail and make the most out of its powerful email automation capabilities.

### Contribution and Support

We welcome contributions from the community to enhance **PyAutoMail** and make it even more robust. If you're interested in contributing, here's how you can get involved:

1. **Bug Reports and Feature Requests**: If you come across any issues or have ideas for new features, please [open an issue](https://github.com/msinamsina/automail/issues) on our GitHub repository. We appreciate detailed bug reports with steps to reproduce the problem and clear feature requests with use cases.

2. **Pull Requests**: If you want to contribute code to PyAutoMail, you can do so by submitting a pull request. Please ensure that your code adheres to the existing code style, and include relevant tests to maintain code quality.

3. **Documentation**: Improving the documentation is always valuable. If you find any inconsistencies or areas that need clarification, feel free to submit documentation updates via pull requests.

4. **Spread the Word**: If you find PyAutoMail useful, help us spread the word by sharing it with your peers and on social media platforms.
