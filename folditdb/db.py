from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize DB globally
DB = create_engine(environ['MYSQL_FOLDIT_DB'])

# Create a class that creates new sessions
Session = sessionmaker()
Session.configure(bind=DB)
