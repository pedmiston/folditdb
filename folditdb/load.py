from sqlalchemy.exc import IntegrityError

from folditdb.db import DB, Session
from folditdb.tables import Base
from folditdb.irdata import IRData
from folditdb.pdl import PDL

def load_solution(irdata, session):
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

def load_solutions_from_file(solutions_file):
    Base.metadata.create_all(DB)
    for json_str in open(solutions_file):
        session = Session()
        irdata = IRData.from_json(json_str)
        load_solution(irdata, session)
