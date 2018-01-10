import folditdb
from folditdb import tables
from folditdb.load import load_single_irdata_file
from folditdb.irdata import IRData, PDL, ActionLog
from folditdb.tables import Action


def test_parse_action_string():
    action_str = "|ActionBandAddAtomAtom=6 |ActionBandDelete=5 |ActionDeleteCut=8"
    actions = ActionLog.from_action_string(action_str)
    assert len(actions) == 3
    first_action = actions[0]
    assert first_action.action_name == 'ActionBandAddAtomAtom'
    assert first_action.action_n == 6

def test_parse_empty_action_log():
    irdata = IRData.from_file('tests/test_data/solution_without_action_log.json')
    pdl = PDL.from_irdata(irdata)[0]
    action_logs = ActionLog.from_pdl(pdl)
    assert len(action_logs) == 0

def test_parse_complex_action_string():
    action_str = "Pull_Mode|ACTIVATE=3 Selection_Interface|BringUpTweakWidget=5 Structure_Mode|ACTIVATE=3 |=8"
    actions = ActionLog.from_action_string(action_str)
    assert len(actions) == 4
    assert actions[0].action_name == 'Pull_ModeACTIVATE'
    assert actions[0].action_n == 3
    assert actions[1].action_name == 'Selection_InterfaceBringUpTweakWidget'
    assert actions[-1].action_name == 'UnknownAction'
    assert actions[-1].action_n == 8

def test_actions_are_parsed_from_solution_with_two_players(tmp_log, session):
    load_single_irdata_file('tests/test_data/solution_with_two_players.json', session)
    player = session.query(tables.Player).filter_by(name='Blipperman').first()
    first_action = player.actions[0]
    assert first_action.action_name == 'ActionBandAddAtomAtom'
    assert first_action.action_n == 6

def test_duplicate_actions_per_player_are_created(tmp_log, session):
    load_single_irdata_file('tests/test_data/multiple_pdls_same_player.json', session)
    player = session.query(tables.Player).filter_by(name='Mark-').first()
    dup_actions = session.query(tables.Action).filter_by(player_id=player.id, action_name='ActionStandaloneResetRecentBest').all()
    assert len(dup_actions) == 2
    assert dup_actions[0].action_n == 200
    assert dup_actions[1].action_n == 519

def test_duplicate_pdls_per_player_are_created(tmp_log, session):
    load_single_irdata_file('tests/test_data/multiple_pdls_same_player_continued.json', session)
    player = session.query(tables.Player).filter_by(name='Mark-').first()
    dup_actions = session.query(tables.Action).filter_by(player_id=player.id, action_name='Design_ModeACTIVATE').all()
    assert len(dup_actions) == 7
