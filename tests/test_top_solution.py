import pytest

from folditdb import tables
from folditdb.load import load_from_irdata
from folditdb.irdata import IRData

@pytest.fixture
def top_solution_irdata():
    return IRData.from_file('tests/test_data/top_solution.json')

def test_create_solution_model_from_top_solution(top_solution_irdata):
    solution = tables.Solution.from_irdata(top_solution_irdata)
    assert solution.solution_type == 'top'
    assert solution.history_id == 'V3'

def test_loading_top_solution_loads_histories(top_solution_irdata, session):
    load_from_irdata(top_solution_irdata, session)

    results = session.query(tables.History).all()
    assert len(results) == 4

def test_loading_top_solutions_with_overlapping_histories(session):
    irdatas = IRData.from_scrape_file('tests/test_data/top_solutions_with_overlapping_histories.json')
    for irdata in irdatas:
        load_from_irdata(irdata, session)

    results = session.query(tables.History).all()
    assert len(results) == 5
