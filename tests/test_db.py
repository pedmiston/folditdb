from os import environ

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from folditdb.db import Base, Solution
from folditdb.solution import SolutionData
from folditdb.scores import add_score


@pytest.fixture(scope='module')
def session():
    DB = create_engine(environ['MYSQL_FOLDIT_TEST_DB'])
    Base.metadata.create_all(DB)
    Session = sessionmaker()
    Session.configure(bind=DB)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(DB)

def test_put_scores_in_db(session):
    data = dict(HISTORY='1,2,3', SCORE='134.2')
    solution = SolutionData(data)
    add_score(solution, session)
    session.commit()

    results = session.query(Solution)
    assert len(results.all()) == 1
    score = results.first()
    assert score.id == '3'
    assert score.score == 134.2
