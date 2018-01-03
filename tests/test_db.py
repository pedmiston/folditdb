from folditdb.irdata import IRData
from folditdb.pdl import PDL
from folditdb.tables import Solution, Player
from folditdb.load import load_solution

def test_load_solution_in_db(session, data):
    load_solution(data, session)

    results = session.query(Solution)
    assert len(results.all()) == 1
    solution = results.first()
    assert solution.id == 1
    assert solution.score == 134.2

def test_load_players_in_db(session, data):
    load_solution(data, session)

    results = session.query(Solution)
    assert len(results.all()) == 1
    solution = results.first()

    results = session.query(Player)
    assert len(results.all()) == 1
    player = results.first()
    assert player.id == 100
    assert len(player.solutions) == 1
    assert solution in player.solutions
