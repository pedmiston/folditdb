from folditdb import tables
from folditdb.irdata import IRData, PDL

def test_create_player_object(irdata):
    pdl = irdata.pdls()[0]
    player = tables.Player.from_pdl(pdl)
    assert player.id == 100
    assert player.name == "bill"
    assert player.team_id == 200

def test_read_solution_with_multiple_players():
    json_filepath = 'tests/test_data/solution_with_two_players.json'
    irdata = IRData.from_file(json_filepath)
    pdls = irdata.pdls()
    assert len(pdls) == 2

    pdl0 = pdls[0]
    assert pdl0.player_name == "Blipperman"

    pdl1 = pdls[1]
    assert pdl1.player_name == "Skippysk8s"
