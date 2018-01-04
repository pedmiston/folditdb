from folditdb.irdata import PDL

def load_solution(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    # Create model objects from the IRData
    puzzle = irdata.to_model_object('Puzzle')
    solution = irdata.to_model_object('Solution')

    # Merge the new objects in the current session.
    # Order matters because the solutions table has a ForeignKey
    # to the puzzles table.
    puzzle = session.merge(puzzle)
    solution = session.merge(solution)

    for pdl in irdata.pdls():
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
