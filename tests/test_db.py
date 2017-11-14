from os import environ
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from folditdb.db import Base, Score
from folditdb.solution import Solution

DB = sqlalchemy.create_engine(environ['MYSQL_FOLDIT_TEST_DB'])
Base.metadata.create_all(DB)
Session = sessionmaker()
Session.configure(bind=DB)

def test_put_scores_in_db():
    s = Session()
    data = dict(HISTORY='1,2,3', SCORE='134.2')
    solution = Solution(data)
    score = solution.to_score_obj()
    s.add(score)
    s.commit()

    results = s.query(Score)
    assert len(results.all()) == 1
    score_2 = results.first()
    assert score == score_2

    s.delete(score)
    s.commit()
    s.close()
