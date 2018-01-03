from folditdb.irdata import IRData

def test_create_irdata_object(data):
    irdata = IRData(data)
    assert irdata.solution_id == 1
    assert irdata.puzzle_id == 1
    assert irdata.history_id == "V3"

def test_create_solution_object(data):
    irdata = IRData(data)
    solution = irdata.to_model_object('Solution')
    assert solution.id == 1
    assert solution.puzzle_id == 1
    assert solution.history_id == "V3"
