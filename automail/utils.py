import logging
import sys


def init_logger(name=''):
    """This function will initialize a logger object
    :param name: the name of the logger
    :type name: str
    :return: logger object
    :rtype: logging.Logger
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

