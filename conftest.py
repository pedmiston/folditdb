from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from folditdb.tables import Base
from folditdb.irdata import IRData


_solution_data = dict(
    SID='1',
    PID='1',
    HISTORY='V1:10,V2:5,V3:4',
    SCORE='134.2',
    PDL='. bill,myteam,100,200',
)

_solution_data_with_multiple_players = dict(
    SID='1',
    PID='1',
    HISTORY='V1:10,V2:5,V3:4',
    SCORE='134.2',
    PDL=[
        '. bill,myteam,100,200',
        '. jim,myteam,101,200',
    ],
)


@pytest.fixture
def solution_data():
    return _solution_data

@pytest.fixture
def solution_data_with_multiple_players():
    return _solution_data_with_multiple_players

@pytest.fixture
def irdata():
    return IRData(_solution_data)

@pytest.fixture
def irdata_with_multiple_players():
    return IRData(_solution_data_with_multiple_players)

@pytest.fixture
def session():
    DB = create_engine(environ['MYSQL_FOLDIT_TEST_DB'])
    Base.metadata.create_all(DB)
    Session = sessionmaker()
    Session.configure(bind=DB)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(DB)
