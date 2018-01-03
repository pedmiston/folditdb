from folditdb.irdata import IRData
from folditdb.tables import Solution

def test_put_scores_in_db(session, data):
    irdata = IRData(data)

    solution = irdata.to_model_object('Solution')
    puzzle = irdata.to_model_object('Puzzle')

    session.add(solution)
    session.add(puzzle)

    session.commit()

    results = session.query(Solution)
    assert len(results.all()) == 1
    score = results.first()
    assert score.id == 1
    assert score.score == 134.2
