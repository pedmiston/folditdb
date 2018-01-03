from folditdb.irdata import IRData
from folditdb.pdl import PDL

def test_create_irdata_object(irdata):
    assert irdata.solution_id == 1
    assert irdata.puzzle_id == 1
    assert irdata.history_id == "V3"

def test_create_solution_object(irdata):
    solution = irdata.to_model_object('Solution')
    assert solution.id == 1
    assert solution.puzzle_id == 1
    assert solution.history_id == "V3"

def test_read_single_solution_from_file():
    json_filepath = 'tests/test_data/single_solution.json'
    irdata = IRData.from_file(json_filepath)
    assert irdata.solution_id == 356820465
