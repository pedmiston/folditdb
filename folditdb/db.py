from os import environ
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()

class Score(Base):
    __tablename__ = 'Scores'
    id = Column(String(60), primary_key=True, nullable=False)
    score = Column(Float)

DB = sqlalchemy.create_engine(environ['MYSQL_FOLDIT_DB'])
# Create tables that do not exist yet
Base.metadata.create_all(DB)
