import json
import logging

from folditdb import tables

logger = logging.getLogger(__name__)


class IRDataCreationError(Exception):
    pass

class PDLCreationError(Exception):
    pass


class IRData:
    """IRData objects facilite the transfer of IRData to model objects.

    Each IRData object corresponds to the data contained in a single
    solution pdb file stored on the Foldit analytics server. The
    solution pdb files were scraped with the foldit-go program command
    'scrape' and consist of all lines in the PDB file that start with
    "IRDATA".

    IRData objects store their IRData as an internal dict, and expose
    output values as properties on the object.

    > json_str = '{"FILEPATH": "/location/of/solution.pdb"}'
    > irdata = IRData.from_json(json_str)
    > irdata.filename == '/location/of/solution.pdb'

    Note that "FILEPATH" in the input is accessed as "filename" in the output.
    This allows more complicated properties to be derived from the internal
    data.

    > json_str = '{"HISTORY": "V1:10,V2:5,V3:8"}'
    > irdata = IRData.from_json(json_str)
    > irdata.history_id == 'V3'

    The reason for using IRData objects is to facilitate the translation
    of the same json data into multiple model objects without redundantly
    processing the same data.

    > from folditdb import tables
    > irdata = IRData.from_file('solution.json')
    > puzzle = tables.Puzzle.from_irdata(irdata)
    > solution = tables.Solution.from_irdata(irdata)

    A few notes about IRData object properties:
    - Properties are computed once and cached.
    - Properties return None if they cannot be computed.
    - If a property cannot be computed, an error is printed to the module logger.
    """
    def __init__(self, data):
        """Create an IRData object from a dict of IRData strings."""
        self._data = data
        self._cache = {}

    @classmethod
    def from_json(cls, json_str):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as err:
            raise IRDataCreationError('bad JSON')
        return cls(data)

    @classmethod
    def from_file(cls, json_filepath):
        with open(json_filepath) as json_file:
            json_str = json_file.read()
            return cls.from_json(json_str)

    @classmethod
    def from_scrape_file(cls, scrape_filepath):
        """Yield IRData objects for each line of json in a scrape file.

        A scrape file is the output of the foldit-go command 'scrape'.
        """
        with open(scrape_filepath) as scrape_file:
            for json_str in scrape_file:
                yield cls.from_json(json_str)

    # Begin defining IRData properties -------------------------------------------

    @property
    def filename(self):
        if 'filename' in self._cache:
            return self._cache['filename']

        filename = self._data.get('FILEPATH')
        if filename is None:
            logger.info('IRData property error: solution has no filepath')

        return self._cache.setdefault('filename', filename)

    @property
    def solution_type(self):
        """Solutions can be "top" or "regular"."""
        if 'solution_type' in self._cache:
            return self._cache['solution_type']

        if self.filename is None:
            solution_type = None
        elif '/top/' in self.filename:
            solution_type = 'top'
        elif '/all/' in self.filename:
            solution_type = 'regular'
        else:
            msg = 'IRData property error: solution type from filename="%s'
            logger.info(msg, self.filename)
            solution_type = None

        return self._cache.setdefault('solution_type', solution_type)

    @property
    def solution_id(self):
        if 'solution_id' in self._cache:
            return self._cache['solution_id']

        # want, have
        solution_id, sid_str = None, self._data.get('SID')

        if sid_str is not None:
            try:
                solution_id = int(sid_str)
            except ValueError:
                msg = 'IRData property error: SID is not an int: SID="%s"'
                logger.info(msg, sid_str, self.filename)
        else:
            msg = 'IRData property error: no solution id, filename="%s"'
            logger.info(msg, self.filename)

        return self._cache.setdefault('solution_id', solution_id)

    @property
    def puzzle_id(self):
        if 'puzzle_id' in self._cache:
            return self._cache['puzzle_id']

        # want, have
        puzzle_id, pid_str = (None, self._data.get('PID'))

        if pid_str is not None:
            try:
                puzzle_id = int(pid_str)
            except ValueError:
                msg = 'IRData property error: PID is not an int: PID="%s"'
                logger.info(msg, pid_str, self.filename)
        else:
            msg = 'IRData property error: no puzzle id: filename="%s"'
            logger.info(msg, self.filename)

        return self._cache.setdefault('puzzle_id', puzzle_id)

    @property
    def history_string(self):
        if 'history_string' in self._cache:
            return self._cache['history_string']

        history_string = self._data.get('HISTORY')
        if history_string is None:
            msg = 'IRData property error: solution has no history: filename="%s"'
            logger.info(msg, self.filename)

        return self._cache.setdefault('history_string', history_string)

    @property
    def history_id(self):
        if 'history_id' in self._cache:
            return self._cache['history_id']

        history_id = None

        if self.history_string is not None:
            # does not fail if history_string is a string
            last_move_in_history = self.history_string.split(',')[-1]
            try:
                history_id, _ = last_move_in_history.split(':')
            except ValueError:
                msg = 'IRData property error: unable to process history string: history_string="%s"'
                logger.info(msg, self.history_string)

        return self._cache.setdefault('history_id', history_id)

    @property
    def total_moves(self):
        if 'total_moves' in self._cache:
            return self._cache['total_moves']

        total_moves = None
        if self.history_string is not None:
            try:
                moves = [int(pair.split(':')[1])
                         for pair in self.history_string.split(',')]
            except (IndexError, ValueError, TypeError):
                msg = 'IRData property error: unable to parse moves from history string: history_string="%s"'
                logger.info(msg, self.history_string)
            else:
                total_moves = sum(moves)

        return self._cache.setdefault('total_moves', total_moves)

    @property
    def score(self):
        if 'score' in self._cache:
            return self._cache['score']

        # want, have
        score, score_str = None, self._data.get('SCORE')

        if score_str is not None:
            try:
                score = float(score_str)
            except ValueError:
                msg = 'IRData property error: SCORE is not a float: score_str="%s"'
                logger.info(msg, score_str)
        else:
            msg = 'IRData property error: missing score: filename="%s"'
            logger.info(msg, self.filename)

        return self._cache.setdefault('score', score)

    def pdls(self):
        if 'pdls' in self._cache:
            return self._cache['pdls']

        pdls = PDL.from_irdata(self)
        return self._cache.setdefault('pdls', pdls)

    def histories(self):
        if 'histories' in self._cache:
            return self._cache['histories']

        histories = History.from_irdata(self)
        return self._cache.setdefault('histories', histories)


class PDL:
    def __init__(self, data):
        self._data = data

    @classmethod
    def from_irdata(cls, irdata):
        pdl_strings = irdata._data.get('PDL')

        if not isinstance(pdl_strings, list):
            pdl_strings = [pdl_strings, ]

        return [cls.from_pdl_string(pdl_str, irdata)
                for pdl_str in pdl_strings]

    @classmethod
    def from_pdl_string(cls, pdl_str, irdata):
        data = {}

        if pdl_str.startswith('. '):
            pdl_str = pdl_str.strip('^. ')
        else:
            msg = 'invalid PDL string: pdl_str="%s"'
            raise PDLCreationError(msg % pdl_str)

        fields = pdl_str.split(',')
        player_name, team_name = fields[:2]
        try:
            player_id, team_id = map(int, fields[2:4])
        except ValueError:
            msg = 'unable to convert player_id and team_id to ints, pdl_str="%s"'
            raise PDLCreationError(msg % pdl_str)

        data = dict(
            player_name=player_name,
            team_name=team_name,
            player_id=player_id,
            team_id=team_id
        )
        return cls(data)

    @property
    def team_type(self):
        if self._data['team_name'] == '[no group]':
            team_type = 'soloist'
        else:
            team_type = 'evolver'
        return team_type

    def __getattr__(self, key):
        return self._data[key]
