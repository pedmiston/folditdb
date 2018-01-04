from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('solution_id', Integer, ForeignKey('solution.id')),
    Column('player_id', Integer, ForeignKey('player.id'))
)

class Puzzle(Base):
    __tablename__ = 'puzzle'
    id = Column(Integer, primary_key=True)
    solutions = relationship('Solution')

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.puzzle_id,
        )
        return cls(**data)


class Solution(Base):
    __tablename__ = 'solution'
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer, ForeignKey('puzzle.id'))
    history_id = Column(String(60))
    moves = Column(Integer)
    score = Column(Float)
    players = relationship('Player', secondary=association_table,
                           backref='solutions')

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.solution_id,
            puzzle_id=irdata.puzzle_id,
            history_id=irdata.history_id,
            moves=irdata.moves,
            score=irdata.score
        )
        return cls(**data)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    players = relationship('Player')

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.team_id,
            name=pdl.team_name
        )
        return cls(**data)


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    team_id = Column(Integer, ForeignKey('team.id'))

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.player_id,
            name=pdl.player_name,
            team_id=pdl.team_id
        )
        return cls(**data)
