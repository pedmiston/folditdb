from folditdb import tables
from folditdb.irdata import IRData, PDL

def test_create_player_object(irdata):
    pdl = PDL.from_irdata(irdata)[0]
    player = tables.Player.from_pdl(pdl)
    assert player.id == 100
    assert player.name == "bill"
    assert player.team_name == "myteam"

def test_read_solution_with_multiple_players():
    json_filepath = 'tests/test_data/solution_with_two_players.json'
    irdata = IRData.from_file(json_filepath)
    pdls = PDL.from_irdata(irdata)
    assert len(pdls) == 2

    pdl0 = pdls[0]
    assert pdl0.player_name == "Blipperman"

    pdl1 = pdls[1]
    assert pdl1.player_name == "Skippysk8s"

def test_rename_team_for_soloist_player():
    json_filepath = 'tests/test_data/soloist_solution.json'
    irdata = IRData.from_file(json_filepath)
    pdl = PDL.from_irdata(irdata)[0]
    team = tables.Team.from_pdl(pdl)
    assert team.name == '[no group]-bill'
