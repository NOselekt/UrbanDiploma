from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

'''Creating an engine for the PostgreSQL database'''
engine = create_engine('postgresql://{user name}:{password}@{host}/{database name}')

'''Creating a session factory from the engine'''
local_session = sessionmaker(bind=engine)
