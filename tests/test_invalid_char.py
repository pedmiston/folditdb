from folditdb.load import load_single_irdata_file

def test_load_solution_file_with_invalid_char(session):
    load_single_irdata_file('tests/test_data/invalid_char.json', session)
