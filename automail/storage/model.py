"""This module contains the classes that are used to store the data in the database

"""
from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import ChoiceType
from automail.storage.util import Base


class Record(Base):
    """This class is used to store the records of the processes in the database table 'record'

    Every record contains the information of one email

    """
    __tablename__ = "record"
    STATUSES = [
        ('unsent', 'Unsent'),
        ('sent', 'Sent')
    ]
    """list : the possible statuses of the record"""
    id = Column(Integer, primary_key=True)
    """int : the id of the record"""
    receiver = Column(String)
    """str : the email address of the receiver"""
    data = Column(String)
    """str : the custom data of the email a string of json"""
    attachment_path = Column(String)
    """str : the path to the attachment file"""
    status = Column(ChoiceType(STATUSES), default='unsent')
    """str : the status of the record it can be choose from STATUSES"""

    process_id = Column(Integer, ForeignKey("process.id"), nullable=False)
    """int : the id of the process which this record belongs to"""
    process = relationship("Process", backref=backref("records", order_by=id))
    """automail.storage.database.Process : the process of the record"""


class Process(Base):
    """This class is used to store the processes of the emails in the database the table name is `process`

    - Every time you register a contact list to send emails to it, a process will be created and stored in the database
    - Every process has a list of records which contains the information of the emails that will be sent
    - The process has a status which can be chosen from STATUSES

    Attributes
    ----------
    records : automail.storage.model.Record
        the records of the process

    """
    __tablename__ = "process"
    STATUSES = [
        ('created', 'Created'),
        ('in progress', 'In progress'),
        ('paused', 'Paused'),
        ('finished', 'Finished')
    ]
    """list : the possible statuses of the process"""
    id = Column(Integer, primary_key=True)
    """int : the id of the process"""
    release_date = Column(Date)
    """datetime.date : the date of the release of the process"""
    sender = Column(String)
    """str : the email address of the sender"""
    temp_file = Column(String)
    """str : the path to the template file"""
    subject = Column(String)
    """str : the subject of the email"""
    status = Column(ChoiceType(STATUSES), default='created')
    """str : the status of the process it can be choose from STATUSES"""
    title = Column(String)
    """str : the title of the process"""
