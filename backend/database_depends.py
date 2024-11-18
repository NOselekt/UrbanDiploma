from sqlalchemy.orm import Session
from backend.database import local_session


def get_database() -> Session:
    '''get_database generates a session for the database'''
    with local_session() as session:
        yield session
