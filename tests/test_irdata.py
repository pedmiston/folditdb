from folditdb import tables
from folditdb.irdata import IRData

def test_create_irdata_object(irdata):
    assert irdata.solution_id == 1
    assert irdata.puzzle_id == 1
    assert irdata.history_id == "V3"
    assert irdata.total_moves == 19

def test_create_solution_object(irdata):
    solution = tables.Solution.from_irdata(irdata)
    assert solution.id == 1
    assert solution.puzzle_id == 1
    assert solution.history_id == "V3"
    assert solution.total_moves == 19

def test_read_single_solution_from_file():
    json_filepath = 'tests/test_data/single_solution.json'
    irdata = IRData.from_file(json_filepath)
    assert irdata.solution_id == 356820465
