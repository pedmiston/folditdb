"""MySQL database table design.

A note on the use of @classmethod:

Most of the table models have class methods for creation.
The reason for this is to provide alternate constructors
for the most common but idiosyncratic ways of creating model
objects. Placing the constructors on the models, rather
than on the objects in folditdb.irdata, allows the
constructor logic to be closest to the model descriptions.
"""
from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Solution(Base):
    __tablename__ = 'solution'
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer(), ForeignKey('puzzle.id'))
    history_id = Column(String(40), ForeignKey('history.id'))
    history_hash = Column(String(64), ForeignKey('history_string.hash'))
    solution_type = Column(String(20))
    total_moves = Column(Integer())
    score = Column(Float())
    timestamp = Column(DateTime())

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.solution_id,
            puzzle_id=irdata.puzzle_id,
            history_id=irdata.history_id,
            solution_type=irdata.solution_type,
            total_moves=irdata.total_moves,
            score=irdata.score,
            timestamp=irdata.timestamp,
        )
        return cls(**data)


class Puzzle(Base):
    __tablename__ = 'puzzle'
    id = Column(Integer, primary_key=True)

    solutions = relationship('Solution')

    @classmethod
    def from_irdata(cls, irdata):
        return cls(id=irdata.puzzle_id)


class History(Base):
    __tablename__ = 'history'
    id = Column(String(40), primary_key=True)

    solutions = relationship('Solution')

    @classmethod
    def last_from_irdata(cls, irdata):
        """Create a history object for the last history in the string."""
        last_history_id = irdata.history_string.split(',')[-1].split(':')[0]
        return cls(id=last_history_id)

    @classmethod
    def from_irdata(cls, irdata):
        """Create a list of History objects from a history string."""
        history_ids = [x.split(':')[0] for x in irdata.history_string.split(',')]
        return [cls(id=history_id) for history_id in history_ids]


class HistoryString(Base):
    __tablename__ = 'history_string'
    hash = Column(String(64), primary_key=True)
    history_string = Column(Text)

    @classmethod
    def from_irdata(cls, irdata):
        return cls(hash=irdata.history_hash, history_string=irdata.history_string)


class Team(Base):
    """Teams are collections of one or more players.

    Team types are evolver or soloists.

    In the IRData, soloist players are represented with a team name of
    '[no group]' and a team id == 0. This is a problem, as it in effect makes a
    huge team of all soloist players. To get around this issue, single-player
    teams are assigned to unique team names based on their player name. This
    means the team id variable is no longer useful, and is not included in the
    model.
    """
    __tablename__ = 'team'
    name = Column(String(60), primary_key=True)
    team_type = Column(String(20))

    players = relationship('Player')
    # puzzles = relationship('Puzzle')

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            name=pdl.team_name,
            team_type=pdl.team_type,
        )
        return cls(**data)


player_solutions = Table('player_solutions', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('solution_id', Integer, ForeignKey('solution.id'))
)

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    team_name = Column(String(60), ForeignKey('team.name'))

    solutions = relationship('Solution',
        secondary=player_solutions,
        backref="players"
    )

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.player_id,
            name=pdl.player_name,
            team_name=pdl.team_name
        )
        return cls(**data)
