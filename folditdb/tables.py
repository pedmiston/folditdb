"""MySQL database table design.

Note on the use of classmethods:
Most of the table models have classmethods for creation.
The reason for this is to provide alternate constructors
for the common, but esoteric, ways of creating model
objects. Placing the constructors on the models, rather
than on the objects in folditdb.irdata, allows the
constructor logic to be closest to the model descriptions.

"""
from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Puzzle(Base):
    __tablename__ = 'puzzle'
    id = Column(Integer, primary_key=True)
    solutions = relationship('Solution')

    @classmethod
    def from_irdata(cls, irdata):
        return cls(id=irdata.puzzle_id)

solutions_and_players = Table('solutions_and_players', Base.metadata,
    Column('solution_id', Integer, ForeignKey('solution.id')),
    Column('player_id', Integer, ForeignKey('player.id')))
# class PlayerSolutions(Base):
#     """Association table for M2M relationship between players and solutions.
#
#     A player has many solutions, and a solution may be submitted by multiple
#     players.
#     """
#     __tablename__ = 'player_solutions'
#     player_id = Column(Integer, ForeignKey('player.id'))
#     solution_id = Column(Integer, ForeignKey('solution.id'))


class SolutionHistory(Base):
    __tablename__ = 'solution_history'
    id = Column(Integer, primary_key=True)
    history_hash = Column(String(40))
    history_string = Column(Text)


class Solution(Base):
    __tablename__ = 'solution'
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer, ForeignKey('puzzle.id'))
    history_id = Column(String(40), ForeignKey('history.id'))
    history_string_id = Column(Integer, ForeignKey('solution_history.id'))
    total_moves = Column(Integer)
    score = Column(Float)
    filename = Column(Text)  # filenames are really long...

    players = relationship('Player', secondary='solutions_and_players',
                           backref='solutions')

    @classmethod
    def from_irdata(cls, irdata):
        data = dict(
            id=irdata.solution_id,
            puzzle_id=irdata.puzzle_id,
            history_id=irdata.history_id,
            total_moves=irdata.total_moves,
            score=irdata.score,
            filename=irdata.filename
        )
        return cls(**data)


# class Edit(Base):
#     """An Edit is a change between solutions.
#
#     Edits are agnostic of their creator, because the ownership of some edits
#     cannot be determined. This is because among teams, solutions with the
#     same history of edits can be shared with other players within the team.
#
#     Each edit actually represents the number of edits between two points: a
#     starting point and an ending point, with a number of moves between.
#     """
#     __tablename__ = 'edit'
#     id = Column(Integer, primary_key=True)
#     history_id = Column(Integer, ForeignKey('history.id'))
#     prev_history_id = Column(Integer, ForeignKey('history.id'))
#     moves = Column(Integer)


class History(Base):
    __tablename__ = 'history'
    id = Column(String(40), primary_key=True)
    solutions = relationship('Solution')

    @classmethod
    def from_irdata(cls, irdata):
        """Create a list of History objects from a history string."""
        history_ids = [x.split(':')[0] for x in history_string.split(',')]
        return [cls(id=history_id) for history_id in history_ids]


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(60))
    team_type = Column(String(20))
    players = relationship('Player')

    @classmethod
    def from_pdl(cls, pdl):
        data = dict(
            id=pdl.team_id,
            name=pdl.team_name,
            team_type=pdl.team_type,
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
