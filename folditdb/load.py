import logging

from folditdb.irdata import IRData, PDL
from folditdb.db import Session
from folditdb.tables import Solution, Puzzle, Team, Player, History

logger = logging.getLogger(__name__)

class DuplicateIRDataException(Exception):
    pass

def load_from_irdata(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    results = session.query(Solution).filter_by(id=irdata.solution_id).all()
    if len(results) > 0:
        raise DuplicateIRDataException

    # Create model objects from IRData
    puzzle = Puzzle.from_irdata(irdata)
    puzzle = session.merge(puzzle)

    # Create a history object for the last history id in this solution.
    # History objects for all history ids in this solution's history string
    # are highly redundant across solutions, and therefore should not
    # be created for all solutions. Instead, history objects will only
    # be made for top ranked solutions.
    last_history = History(id=irdata.history_id)
    session.add(last_history)

    solution = Solution.from_irdata(irdata)
    session.add(solution)

    # Cannot assume one player per solution because
    # some solutions are contributed by more than one player.
    for pdl in irdata.pdls():
        team = Team.from_pdl(pdl)
        player = Player.from_pdl(pdl)

        session.merge(team)
        player = session.merge(player)
        player.solutions.append(solution)

    # if irdata.solution_type == 'top' and irdata.history_string:
    #     for history_id in irdata.histories():
    #         history = History(id=history_id, solution_id=solution.id)
    #         session.add(history)

    session.commit()

    if local_session:
        session.close()

def load_single_irdata_file(solution_file, session=None):
    irdata = IRData.from_file(solution_file)
    load_from_irdata(irdata, session)

def load_irdata_from_file(solutions_file, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    for irdata in IRData.from_scrape_file(solutions_file):
        load_from_irdata(irdata, session)

    session.close()
