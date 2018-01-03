from sqlalchemy.exc import IntegrityError

from folditdb.irdata import IRData
from folditdb.pdl import PDL

def load_solutions(solutions):
    for solution_json in open(solutions):
        solution = IRData.from_json(solution_json)
        print(solution.filename)

def load_solution(data, session):
    irdata = IRData(data)

    solution = irdata.to_model_object('Solution')
    puzzle = irdata.to_model_object('Puzzle')

    session.add(solution)
    session.add(puzzle)

    for pdl_str in irdata.pdl_strings():
        pdl = PDL(pdl_str)

        team = pdl.to_model_object('Team')
        team = session.merge(team)

        player = pdl.to_model_object('Player')
        player = session.merge(player)
        player.solutions.append(solution)
        session.add(player)
