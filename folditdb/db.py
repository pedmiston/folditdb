from os import environ

from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DB = create_engine(environ['MYSQL_FOLDIT_DB'])
Session = sessionmaker()
Session.configure(bind=DB)

Base = declarative_base()

class Puzzle(Base):
    __tablename__ = 'puzzle'
    id = Column(Integer, primary_key=True, nullable=False)
    solutions = relationship('Solution')

class Solution(Base):
    __tablename__ = 'score'
    id = Column(String(60), primary_key=True, nullable=False)
    puzzle_id = Column(Integer, ForeignKey('puzzle.id'))
    score = Column(Float)

# Create tables that do not exist yet
Base.metadata.create_all(DB)
