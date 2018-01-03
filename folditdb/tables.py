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
    player_id = Column(Integer, ForeignKey('player.id'))
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


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(60))
    team_id = Column(Integer, ForeignKey('team.id'))
    solutions = relationship('Solution')

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.player_id,
            name=pdl.player_name,
            team_id=pdl.team_id
        )
        return cls(**data)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(60))
    players = relationship('Player')

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.team_id,
            name=pdl.team_name
        )
        return cls(**data)


# Create tables that do not exist yet
Base.metadata.create_all(DB)
