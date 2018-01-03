from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from folditdb.db import DB

Base = declarative_base()

class Puzzle(Base):
    __tablename__ = 'puzzle'
    id = Column(Integer, primary_key=True, nullable=False)
    solutions = relationship('Solution')

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.puzzle_id,
        )
        return cls(**data)

class Solution(Base):
    __tablename__ = 'solution'
    id = Column(Integer, primary_key=True, nullable=False)
    puzzle_id = Column(Integer, ForeignKey('puzzle.id'))
    history_id = Column(String(60))
    score = Column(Float)

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.solution_id,
            puzzle_id=irdata.puzzle_id,
            history_id=irdata.history_id,
            score=irdata.score
        )
        return cls(**data)

# Create tables that do not exist yet
Base.metadata.create_all(DB)
