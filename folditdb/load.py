import logging
from folditdb.irdata import IRData, PDL
from folditdb.db import Session

logger = logging.getLogger('folditdb')


def load_solution(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    # Create model objects from the IRData
    puzzle = irdata.to_model_object('Puzzle')
    solution = irdata.to_model_object('Solution')

    try:
        # Merge the new objects in the current session.
        # Order matters because the solutions table has a ForeignKey
        # to the puzzles table.
        puzzle = session.merge(puzzle)
        solution = session.merge(solution)

        for pdl in irdata.pdls():
            team = pdl.to_model_object('Team')
            player = pdl.to_model_object('Player')

            try:
                with session.begin_nested():
                    team = session.merge(team)
            except Exception as err:
                logging.info('DB error: merging team: {err}'.format(err))
                continue

            try:
                with session.begin_nested():
                    player = session.merge(player)
            except Exception as err:
                logging.info('DB error: merging player: {err}'.format(err))
                continue

            player.solutions.append(solution)

        session.commit()
    except Exception as err:
        logging.info('Unexpected DB error: {}'.format(err))
        session.rollback()
    finally:
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
            logger.info('Loading error: {}'.format(e))
            continue
