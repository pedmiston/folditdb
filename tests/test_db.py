from os import environ

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from folditdb.db import Base, Score
from folditdb.solution import Solution
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
    solution = Solution(data)
    add_score(solution, session)
    session.commit()

    results = session.query(Score)
    assert len(results.all()) == 1
    score = results.first()
    assert score.id == '3'
    assert score.score == 134.2
