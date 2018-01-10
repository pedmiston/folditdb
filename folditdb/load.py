import logging

from sqlalchemy import exists
from sqlalchemy.exc import DBAPIError

from folditdb.irdata import IRData, PDL, ActionLog
from folditdb.irdata import IRDataPropertyError, IRDataCreationError, PDLCreationError, PDLPropertyError
from folditdb.db import Session
from folditdb.tables import Solution, Puzzle, Team, Player, History, HistoryString, Action

logger = logging.getLogger(__name__)


class DuplicateIRDataException(Exception):
    pass


def load_top_solutions_from_file(top_solutions_file, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    for i, irdata in enumerate(IRData.from_scrape_file(top_solutions_file)):
        try:
            load_from_irdata(irdata, session)
        except DBAPIError as err:
            session.rollback()
            logger.error('%s:%s %s(%s)', top_solutions_file, i+1, err.__class__.__name__, err)
        except Exception as err:
            logger.error('%s:%s %s(%s)', top_solutions_file, i+1, err.__class__.__name__, err)

    session.close()


def load_from_irdata(irdata, session=None):
    local_session = (session is None)
    if local_session:
        session = Session()

    # Create model objects from IRData
    solution = Solution.from_irdata(irdata)
    puzzle = Puzzle.from_irdata(irdata)
    last_history = History.last_from_irdata(irdata)
    history_string = HistoryString.from_irdata(irdata)

    # Check if this solution has already been loaded
    solution_exists = session.query(exists().where(Solution.id == solution.id)).scalar()
    if solution_exists:
        raise DuplicateIRDataException()

    # Add model objects to the current session
    # Order matters!
    puzzle = session.merge(puzzle)
    last_history = session.merge(last_history)
    history_string = session.merge(history_string)
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

        # Load final actions from these players
        for pdl in pdls:
            actions = Action.from_pdl(pdl)
            for action in actions:
                session.merge(action)

    session.commit()

    if local_session:
        session.close()

def load_single_irdata_file(solution_file, session=None):
    irdata = IRData.from_file(solution_file)
    load_from_irdata(irdata, session)
