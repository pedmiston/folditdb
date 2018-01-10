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

def load_from_irdata(irdata, session=None, return_on_error=False):
    local_session = (session is None)
    if local_session:
        session = Session()

    try:
        # Create model objects from IRData
        solution = Solution.from_irdata(irdata)
        puzzle = Puzzle.from_irdata(irdata)
        last_history = History.last_from_irdata(irdata)
        history_string = HistoryString.from_irdata(irdata)
    except IRDataPropertyError:
        if return_on_error:
            return
        else:
            raise

    # Check if this solution has already been loaded
    solution_exists = session.query(exists().where(Solution.id == solution.id)).scalar()
    if solution_exists:
        raise DuplicateIRDataException

    # Add model objects to the current session
    # Order matters!
    puzzle = session.merge(puzzle)
    last_history = session.merge(last_history)
    history_string = session.merge(history_string)
    session.add(solution)

    try:
        pdls = PDL.from_irdata(irdata)
    except PDLCreationError:
        if return_on_error:
            return
        else:
            raise

    for pdl in pdls:
        try:
            team = Team.from_pdl(pdl)
            player = Player.from_pdl(pdl)
        except PDLPropertyError:
            if return_on_error:
                return
            else:
                raise

        session.merge(team)
        player = session.merge(player)
        player.solutions.append(solution)

    if irdata.solution_type == 'top':
        # Load all histories but the last one (which has already been added)
        for history in History.from_irdata(irdata)[:-1]:
            session.merge(history)

        # Load final actions from these players
        for pdl in pdls:
            try:
                actions = Action.from_pdl(pdl)
            except PDLPropertyError:
                if return_on_error:
                    return
                else:
                    raise
            else:
                for action in actions:
                    session.merge(action)

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

    for i, irdata in enumerate(IRData.from_scrape_file(solutions_file)):
        try:
            load_from_irdata(irdata, session)
        except DBAPIError as err:
            if err.connection_invalidated:
                logger.error("Lost connection to DB, trying again")
                session.rollback()
                load_from_irdata(irdata, session, return_on_error=True)
            else:
                raise
        except Exception as err:
            logger.error('%s:%s %s(%s)', solutions_file, i, err.__class__.__name__, err)

    logger.error('Finished loading scape file "%s"', solutions_file)

    session.close()
