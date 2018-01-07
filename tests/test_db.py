import pytest

from folditdb.irdata import IRData, PDL
from folditdb.tables import Solution, Player
from folditdb.load import load_from_irdata, load_single_irdata_file, load_irdata_from_file, DuplicateIRDataException

def test_load_irdata_in_db(irdata, session):
    load_from_irdata(irdata, session)

    results = session.query(Solution)
    assert len(results.all()) == 1
    solution = results.first()
    assert solution.id == 1
    assert solution.score == 134.2
    assert solution.total_moves == 19

    results = session.query(Player)
    assert len(results.all()) == 1
    player = results.first()
    assert player.id == 100

    # Ensure the solution is attached to the player
    assert len(player.solutions) == 1
    assert solution in player.solutions

def test_load_irdata_raises_exception_on_duplicate_solution(irdata, session):
    load_from_irdata(irdata, session)
    with pytest.raises(DuplicateIRDataException):
        load_from_irdata(irdata, session)
    assert len(session.query(Solution).all()) == 1

def test_load_irdata_with_multiple_players_in_db(irdata_with_multiple_players,
        session):
    load_from_irdata(irdata_with_multiple_players, session)
    solution = session.query(Solution).first()
    assert len(solution.players) == 2

def test_load_single_irdata_file(session):
    solution_file = 'tests/test_data/single_solution.json'
    load_single_irdata_file(solution_file, session)
    solution = session.query(Solution).first()
    assert solution.id == 356820465

def test_load_irdata_from_file(session):
    solutions_file = 'tests/test_data/two_solutions_to_same_puzzle.json'
    load_irdata_from_file(solutions_file, session)
    results = session.query(Solution).all()
    assert len(results) == 2

def test_load_soloist_solution_from_file(session):
    solution_file = 'tests/test_data/soloist_solution.json'
    load_single_irdata_file(solution_file, session)
    solution = session.query(Solution).first()
    assert solution.id == 356818458
