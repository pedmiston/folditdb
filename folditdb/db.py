from os import environ

from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB = create_engine(environ['MYSQL_FOLDIT_DB'])
Session = sessionmaker()
Session.configure(bind=DB)

Base = declarative_base()

class Score(Base):
    __tablename__ = 'Scores'
    id = Column(String(60), primary_key=True, nullable=False)
    score = Column(Float)

# Create tables that do not exist yet
Base.metadata.create_all(DB)
