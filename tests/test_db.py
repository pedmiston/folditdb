from folditdb.irdata import IRData
from folditdb.pdl import PDL
from folditdb.tables import Solution

def test_put_scores_in_db(session, data):
    irdata = IRData(data)

    solution = irdata.to_model_object('Solution')
    puzzle = irdata.to_model_object('Puzzle')

    session.add(solution)
    session.add(puzzle)

    for pdl_str in irdata.pdl_strings():
        pdl = PDL(pdl_str)

        player = pdl.to_model_object('Player')
        team = pdl.to_model_object('Team')

        session.add(player)
        session.add(team)

    session.commit()

    results = session.query(Solution)
    assert len(results.all()) == 1
    score = results.first()
    assert score.id == 1
    assert score.score == 134.2
