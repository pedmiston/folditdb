import logging

from sqlalchemy import exists

from folditdb.irdata import IRData, PDL, IRDataPropertyError
from folditdb.db import Session
from folditdb.tables import Solution, Puzzle, Team, Player, History

logger = logging.getLogger(__name__)

class DuplicateIRDataException(Exception):
    pass

def load_from_irdata(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    # Create model objects from IRData
    solution = Solution.from_irdata(irdata)
    puzzle = Puzzle.from_irdata(irdata)
    last_history = History.last_from_irdata(irdata)

    # Check if this solution has already been loaded
    solution_exists = session.query(exists().where(Solution.id == solution.id)).scalar()
    if solution_exists:
        raise DuplicateIRDataException

    # Add model objects to the current session
    # Order matters!
    puzzle = session.merge(puzzle)
    session.add(last_history)
    session.add(solution)

    pdls = PDL.from_irdata(irdata)
    for pdl in pdls:
        team = Team.from_pdl(pdl)
        player = Player.from_pdl(pdl)

        session.merge(team)
        player = session.merge(player)
        player.solutions.append(solution)

    if irdata.solution_type == 'top':
        # Load all histories but the last one (which has already been added)
        for history in History.from_irdata(irdata)[:-1]:
            session.merge(history)

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
