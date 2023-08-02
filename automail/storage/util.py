from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
import datetime
import pandas as pd

Base = declarative_base()


def create_tables(engine):
    """create tables in database

    Parameters
    ----------
    engine: sqlalchemy.engine.base.Engine
        an engine from database

    Returns
    -------
    None

    Examples
    --------
    >>> create_tables(engine)
    """
    Base.metadata.create_all(engine)


def get_session():
    """get a session from database

    Returns
    -------
    session: sqlalchemy.orm.session.Session
        a session from database
    engine: sqlalchemy.engine.base.Engine
        an engine from database

    Examples
    --------
    >>> get_session()
    (<sqlalchemy.orm.session.Session object at 0x0000020F4F6F6F98>, <sqlalchemy.engine.base.Engine object at 0x0000020F4F6F6F28>)
    """
    engine = create_engine('sqlite:///mail.db', echo=False)

    # create a Session
    session = sessionmaker(bind=engine)
    session = session()
    return session, engine


def register_new_process(title, subject, email, template, contact_list, custom_pdf, attachment, custom_pdf_dir):
    """register a new process in database

    Parameters
    ----------
    title: str
        title of the process
    subject: str
        subject of the process
    email: str
        email of the sender
    template: str
        path to the template
    contact_list: str
        path to the contact list
    custom_pdf: bool
        if True, convert the contact list to pdf
    attachment: str
        path to the attachment
    custom_pdf_dir: str
        path to the custom pdf

    Returns
    -------
    None

    Examples
    --------
    >>> register_new_process(title="test", subject="test", email="test", template="test",\
     contact_list="test", custom_pdf=False, attachment=None, custom_pdf_dir=None)
    """
    from automail.storage import Record, Process

    session, engin = get_session()
    create_tables(engin)

    process = Process(title=title, subject=subject, sender=email,
                      temp_file=template, release_date=datetime.datetime.date(datetime.datetime.now()))

    session.add(process)
    session.commit()

    print(f"ID:{process.id} => Registering user {email} with contacts {contact_list}")
    contact_df = pd.read_csv(contact_list)
    for index, row in contact_df.iterrows():
        filename = None
        if attachment:
            filename = attachment.strip()

        if custom_pdf:
            filename = os.path.join(custom_pdf_dir, str(row['cpdf']) + '.pdf')
        email = row['email'].strip()
        record = Record(receiver=email, data=row.to_json(), process_id=process.id, attachment_path=filename)
        session.add(record)
        session.commit()
        print(f"ID:{record.id} => Registering record for {email}")

    session.close()
    engin.dispose()
