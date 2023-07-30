from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


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