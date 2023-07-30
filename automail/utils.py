import logging
import sys


def init_logger(name=''):
    """This function will initialize a logger object

    Parameters
    ----------
    name : str
        The name of the logger object. If not specified, the name will be the root logger.

    Returns
    -------
    logger_obj : logging.Logger
        The logger object.

    Notes
    -----
    This function will initialize a logger object with the following format::

        [%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s


    Example
    -------
    The logger object will log to both stdout and a file.
    After colling this function you can use logger_obj to log.

    >>> logger_obj = init_logger('EmailSender')
    >>> logger_obj.debug('debug message')
    [2019-08-20 15:30:00,000 - DEBUG (EmailSender) ] : debug message
    >>> logger_obj.info('info message')
    [2019-08-20 15:30:00,000 - INFO (EmailSender) ] : info message
    >>> logger_obj.warning('warning message')
    [2019-08-20 15:30:00,000 - WARNING (EmailSender) ] : warning message
    >>> logger_obj.error('error message')
    [2019-08-20 15:30:00,000 - ERROR (EmailSender) ] : error message
    >>> logger_obj.critical('critical message')
    [2019-08-20 15:30:00,000 - CRITICAL (EmailSender) ] : critical message


    """
    logger_obj = logging.getLogger(name)
    logger_obj.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s')
    handler1 = logging.StreamHandler(sys.stdout)
    handler1.setFormatter(formatter)
    handler2 = logging.FileHandler('../emailsender.log')
    handler2.setFormatter(formatter)
    logger_obj.addHandler(handler1)
    logger_obj.addHandler(handler2)
    return logger_obj

