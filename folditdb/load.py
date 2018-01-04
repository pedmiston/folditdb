from sys import stderr

from folditdb.db import DB, Session
from folditdb.tables import Base
from folditdb.irdata import IRData
from folditdb.pdl import PDL

def load_solution(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    solution = irdata.to_model_object('Solution')
    puzzle = irdata.to_model_object('Puzzle')

    puzzle = session.merge(puzzle)
    solution = session.merge(solution)

    for pdl_str in irdata.pdl_strings():
        pdl = PDL(pdl_str)

        team = pdl.to_model_object('Team')
        team = session.merge(team)

        player = pdl.to_model_object('Player')
        player = session.merge(player)
        player.solutions.append(solution)
        player = session.merge(player)

    session.commit()

    if local_session:
        session.close()

def load_single_solution_from_file(solution_file, session=None):
    irdata = IRData.from_file(solution_file)
    load_solution(irdata, session)

def load_solutions_from_file(solutions_file, session=None):
    for i, json_str in enumerate(open(solutions_file)):
        irdata = IRData.from_json(json_str)

        try:
            load_solution(irdata, session)
        except Exception as e:
            stderr.write('{solutions_file}, {i}, {e}'.format(solutions_file=solutions_file, i=i, e=e))
            continue
