from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy_utils import ChoiceType

engine = create_engine('sqlite:///mail.db', echo=False)
Base = declarative_base()

# create a Session
Session = sessionmaker(bind=engine)
session = Session()


class Record(Base):
    """a record of E-mail

    Attributes:
        id (int): id of record
        receiver (str): receiver of E-mail
        data (str): data of E-mail (string of dict)
        attachment_path (str): path to attachment file

    """
    __tablename__ = "record"
    STATUSES = [
        ('unsent', 'Unsent'),
        ('sent', 'Sent')
    ]

    id = Column(Integer, primary_key=True)
    receiver = Column(String)
    data = Column(String)
    attachment_path = Column(String)
    status = Column(ChoiceType(STATUSES), default='unsent')

    process_id = Column(Integer, ForeignKey("process.id"))
    process = relationship("Process", backref=backref("records", order_by=id))


class Process(Base):
    """"""
    __tablename__ = "process"

    STATUSES = [
        ('created', 'Created'),
        ('in progress', 'In progress'),
        ('paused', 'Paused'),
        ('finished', 'Finished')
    ]

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    sender = Column(String)
    temp_file = Column(String)
    subject = Column(String)
    status = Column(ChoiceType(STATUSES), default='created')


# create tables
Base.metadata.create_all(engine)
