from datetime import datetime

import pytest

from folditdb import tables
from folditdb.irdata import IRData, IRDataPropertyError

def test_irdata_properties(irdata):
    assert irdata.solution_id == 1
    assert irdata.puzzle_id == 1
    assert irdata.history_id == "V3"
    assert irdata.total_moves == 19

def test_solution_model_fields(solution):
    assert solution.id == 1
    assert solution.puzzle_id == 1
    assert solution.history_id == "V3"
    assert solution.total_moves == 19

def test_solution_has_timestamp(solution):
    assert solution.timestamp == datetime.fromtimestamp(0)

def test_read_single_solution_from_file():
    json_filepath = 'tests/test_data/single_solution.json'
    irdata = IRData.from_file(json_filepath)
    assert irdata.solution_id == 356820465

def test_error_when_solution_without_history():
    irdata = IRData.from_file('tests/test_data/solution_without_history.json')
    with pytest.raises(IRDataPropertyError):
        tables.Solution.from_irdata(irdata)
