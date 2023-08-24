import smtplib
import os
import jinja2
import json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser
from pyautomail.config import configurable
from pyautomail.utils import init_logger


__all__ = ['EmailSender']


class EmailSender:
    """ This class is for sending emails to multiple users.

    This class uses a template engine to render the email body. Currently, it supports two template types: '.txt' and
    '.html'. You can use the template type that suits your needs. The template engine that is used in this class is
    Jinja2. You can find more information about Jinja2 in the following link:
    https://jinja.palletsprojects.com/en/2.11.x/

    Examples
    --------
    >>> from pyautomail import EmailSender
    >>> sender = EmailSender(cfg="config.cfg")
    >>> sender.set_template('body.txt')
    >>> data = {'name': 'Jon', 'age': 30}
    >>> sender.send('contact1@gmail.com', 'sub1', data)

    a simple example of a template file:

    body.txt:

    .. code-block:: text

        Hello {{name}}, your age is {{age}}.

    a simple example of a config.cfg file:

    .. code-block:: ini

        [smtp]
        host = smtp.gmail.com
        port = 465
        is_test = True

        [account]
        user = ""
        password = ""

    Or you can use the class without a config file::

        from automail import EmailSender
        sender = EmailSender(user="your-email-address", password="your-password")
        sender.set_template('body.txt')
        data = {'name': 'Jon', 'age': 30}
        sender.send('contact1@gmail.com', 'sub1', data)

    .. _NumPy Documentation HOWTO:
        https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

    """

    @configurable
    def __init__(self, user, password, host="smtp.gmail.com", port=465, is_test=False, log_file=None, log_level=10):
        """
        Parameters
        ----------
        user : str
            The email address of the sender.
        password : str
            The password of the sender.
        host : str
            The host of the SMTP server.
        port : int
            The port of the SMTP server.
        is_test : bool
            If this flag is set, no email will be sent. This flag is useful for testing purposes.
        log_file : str
            The path to the log file.
        log_level : int
            The level of the logger. The default value is 100. You can use the following values:

            - 10: DEBUG
            - 20: INFO
            - 30: WARNING
            - 40: ERROR
            - 50: CRITICAL
        """
        self.__logger = init_logger('EmailSender', filename=log_file, level=log_level)
        self.__logger.info("Initializing EmailSender...")
        self.template_type = None
        self.template = None
        self.__test_flg = is_test
        self.user = user
        self.host = host
        self.port = port
        self.password = None
        if not self.__test_flg:
            self.__logger.info("Connecting to SMTP server...")
            self.password = password
            self.server = smtplib.SMTP_SSL(self.host, self.port)
            self.__logger.info("Connected to SMTP server.")
            self.__logger.info(f"Logging in to user account: {self.user}...")
            try:
                self.server.login(self.user, self.password)
                self.__logger.info("Logged in.")
            except smtplib.SMTPException as e:
                self.__logger.error('Authentication ERROR: Username and Password not accepted. '
                                    'Please check username and password and try again')
                self.__logger.debug(self.password)
                exit(1)
        else:
            self.__logger.warning("Test Mode is enabled. In this mode no email will be sent.")
            self.__logger.warning("To disable test mode, set is_test=False when initializing this class.")
            self.__logger.warning(f"user account: {self.user}...")

    def __del__(self):
        """This function is called when the class is destroyed.
        """
        if not self.__test_flg:
            self.__logger.info("Closing connection to SMTP server...")
            self.server.close()
            self.__logger.info("Connection closed.")

    @classmethod
    def from_config(cls, cfg=None):
        """This method is used to initialize this class from a config file.
        """
        if cfg is None:
            return {}

        if os.path.exists(cfg):
            config = ConfigParser()
            config.read(cfg)
        else:
            return {}

        host = config.get('smtp', 'host')
        port = config.getint('smtp', 'port')
        is_test = config.getboolean('smtp', 'is_test')
        user = config.get('account', 'user')
        password = config.get('account', 'password')
        log_file = config.get('log', 'file-path')
        log_level = config.getint('log', 'level')

        return {'host': host, 'port': port, 'user': user, 'password': password,
                'is_test': is_test, 'log_file': log_file, 'log_level': log_level}

    def set_template(self, template_path=None, plain_temp=None):
        """

        :param template_path: Path to template file. the template file should be either HTML or TXT.
        :param plain_temp: A string template.
        :raises: NotImplemented if template type is not supported.
        """
        assert template_path is not None or plain_temp is not None,\
            "one of 'template_path' or 'plain_temp' should be set"

        if template_path is not None:
            with open(template_path) as f:
                self.template = f.read()

            if template_path.endswith('.html'):
                self.template_type = 'html'
            elif template_path.endswith('.txt'):
                self.template_type = 'txt'
            else:
                self.__logger.error("Template type not supported! Exiting! (please use HTML or TXT templates.)")
                raise (NotImplemented, "Template type not supported! Exiting! (please use HTML or TXT templates.)")
        elif plain_temp is not None:
            self.template = plain_temp
            self.template_type = 'plain'

    def render_template(self, data):
        """This method is used by send method.

        :param data: dictionary of data to be replaced in the template.
        :return: body: the string of the rendered template.
        """
        if isinstance(data, str):
            data = json.loads(data)
        if self.template_type == 'html':
            self.__logger.debug("Rendering HTML template...")
            return jinja2.Template(self.template).render(data)
        elif self.template_type == 'txt':
            self.__logger.debug("Rendering TXT template...")
            return jinja2.Template(self.template).render(data)
        elif self.template_type == 'plain':
            self.__logger.debug("Rendering plain template...")
            return jinja2.Template(self.template).render(data)
        else:
            self.__logger.error("Template type not supported! Exiting! (please use HTML or TXT templates.)")
            raise (NotImplemented, "Template type not supported! Exiting! (please use HTML or TXT templates.)")

    def send(self, receiver_email_address: str, subject: str,
             data: dict, attachment_path=None, from_address=None) -> dict:
        """

        :param receiver_email_address: Email address of the receiver.
        :param subject: Subject of the email.
        :param data: dictionary of data to be replaced in the template.
        :param attachment_path: Path to attachment file.
        :param from_address: Email address of the sender.
        :return:
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["To"] = receiver_email_address
        if from_address is None:
            message["From"] = self.user
        else:
            message["From"] = from_address
        if self.template_type is not None:
            body = self.render_template(data)
            if self.template_type == 'html':
                message.attach(MIMEText(body, "html"))
            elif self.template_type == 'txt':
                message.attach(MIMEText(body, "plain"))
            elif self.template_type == 'plain':
                message.attach(MIMEText(body, "plain"))
        else:
            self.__logger.warning("No template is set. Sending email with no body.")
            body = ''

        if attachment_path:
            filename = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)

        try:
            self.__logger.info("Sending email to: " + receiver_email_address + " message:\n" + body[0:1000] + "...\n")
            if self.__test_flg:
                output = {'test': True}
            else:
                output = self.server.sendmail(self.user, receiver_email_address, message.as_string())
                output['test'] = False
                output['err'] = 'none'
        except Exception as e:
            self.__logger.error("Error sending email to: " + receiver_email_address + " error: " + str(e))
            return {'test': self.__test_flg, 'err': str(e)}
        return output
