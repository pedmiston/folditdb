from folditdb.irdata import IRData
from folditdb.pdl import PDL

def test_create_player_object(data):
    irdata = IRData(data)
    pdl = PDL(irdata.pdl_strings()[0])
    player = pdl.to_model_object('Player')
    assert player.id == 100
    assert player.name == "bill"
    assert player.team_id == 200

def test_read_solution_with_multiple_players():
    json_filepath = 'tests/test_data/solution_with_two_players.json'
    irdata = IRData.from_file(json_filepath)
    pdl_strings = irdata.pdl_strings()
    assert len(pdl_strings) == 2

    pdl0 = PDL(pdl_strings[0])
    assert pdl0.player_name == "Blipperman"

    pdl1 = PDL(pdl_strings[1])
    assert pdl1.player_name == "Skippysk8s"
