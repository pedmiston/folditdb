"""MySQL database table design.

A note on the use of @classmethod:

Most of the table models have class methods for creation.
The reason for this is to provide alternate constructors
for the most common but idiosyncratic ways of creating model
objects. Placing the constructors on the models, rather
than on the objects in folditdb/irdata.py, allows the
constructor logic to be closest to the model descriptions.
"""
from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IRData(Base):
    """An IRData is created from a solution pdb file."""
    __tablename__ = 'irdata'
    irdata_id = Column(Integer(), primary_key=True)
    filename = Column(String(100), index=True)
    data = Column(Text())
    file_type = Column(String(10))

    @classmethod
    def from_irdata(cls, irdata):
        return cls(filename=irdata.filename,
                   data=irdata.json_str,
                   file_type=irdata.file_type)

class Competition(Base):
    """A competition is a team competing in a puzzle."""
    __tablename__ = 'competition'
    competition_id = Column(Integer(), primary_key=True)
    team_id = Column(Integer(), ForeignKey('team.team_id'))
    puzzle_id = Column(Integer(), ForeignKey('puzzle.puzzle_id'))

    @classmethod
    def from_irdata(cls, irdata):
        return cls(puzzle_id=irdata.puzzle_id,
                   team_id=irdata.team_id)

class Submission(Base):
    """A submission is a solution submitted in a competition."""
    __tablename__ = 'submission'
    submission_id = Column(Integer(), primary_key=True)
    competition_id = Column(Integer(), ForeignKey('competition.competition_id'))
    solution_id = Column(Integer(), ForeignKey('solution_history.solution_history_id'))
    timestamp = Column(DateTime(), nullable=False)

    @classmethod
    def from_irdata(cls, irdata, **kwargs):
        kwargs.update(dict(timestamp=irdata.timestamp,
                           history_data=irdata.history_string,
                           score=irdata.score))
        return cls(**kwargs)

class TopSubmission(Base):
    """A top submission is a submission with rank information."""
    __tablename__ = 'top_submission'
    submission_id = Column(Integer(), ForeignKey('submission.submission_id'), primary_key=True)
    rank_type = Column(String(10))
    rank = Column(Integer())

    @classmethod
    def from_irdata(cls, irdata, **kwargs):
        kwargs.update(dict(rank_type=irdata.rank_type,
                           rank=irdata.rank))
        return cls(**kwargs)

class Solution(Base):
    """A solution is a molecule with a particular history."""
    __tablename__ = 'solution'
    solution_id = Column(Integer(), primary_key=True)
    molecule_id = Column(Integer(), ForeignKey('molecule.molecule_id'))
    history_id = Column(Integer(), ForeignKey('history.history_id'))

class History(Base):
    """A history is a sequence of edits."""
    __tablename__ = 'history'
    history_id = Column(Integer(), primary_key=True)
    history_data = Column(Text())
    history_hash = Column(String(64), unique=True)
    total_moves = Column(Integer())
    edits = relationship('Edit')

class Edit(Base):
    """An edit is a change from one molecule to another."""
    __tablename__ = 'edit'
    edit_id = Column(Integer(), primary_key=True)
    molecule_id = Column(Integer(), ForeignKey('molecule.molecule_id'))
    prev_molecule_id = Column(Integer(), ForeignKey('molecule.molecule_id'))
    moves = Column(Integer())

class Molecule(Base):
    """A molecule is the basis for scoring and ranking solutions."""
    __tablename__ = 'molecule'
    molecule_id = Column(Integer(), primary_key=True)
    molecule_hash = Column(String(40), unique=True)
    score = Column(Float())

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
    actions = relationship('Action')

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

class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer(), primary_key=True)
    action_name = Column(String(55))
    action_n = Column(Integer())
    player_id = Column(Integer(), ForeignKey('player.id'))
    puzzle_id = Column(Integer(), ForeignKey('puzzle.id'))

    @classmethod
    def from_pdl(cls, pdl):
        actions = []
        for action_log in pdl.action_logs():
            data = dict(
                action_name=action_log.action_name,
                action_n=action_log.action_n,
                player_id=pdl.player_id,
                puzzle_id=pdl._irdata.puzzle_id
            )
            actions.append(cls(**data))
        return actions
