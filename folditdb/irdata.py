import json
import logging

from folditdb import tables

logger = logging.getLogger('folditdb')

class IRDataCreationError(Exception):
    pass

class PDLCreationError(Exception):
    pass


class IRData:
    """IRData objects facilite the transfer of IRData to model objects.

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

    > irdata = IRData.from_file('solution.json')
    > puzzle = irdata.to_model_obj('Puzzle')
    > solution = irdata.to_model_obj('Solution')
    """
    def __init__(self, data):
        """Create an IRData object from a dict of IRData keys and values."""
        self._data = data

    @classmethod
    def from_json(cls, json_str):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as err:
            raise IRDataCreationError('bad JSON')
        return cls(data)

    @classmethod
    def from_file(cls, json_filepath):
        with open(json_filepath) as f:
            return cls.from_json(f.read())

    @property
    def filename(self):
        if hasattr(self, '_filename'):
            return self._filename

        self._filename = self._data.get('FILEPATH')
        if self._filename is None:
            logger.info('IRData property error: solution has no filepath')
        return self._filename

    @property
    def solution_type(self):
        """Solutions can be "top" or "regular"."""
        if hasattr(self, '_solution_type'):
            return self._solution_type

        if self.filename is None:
            self._solution_type = None
        elif '/top/' in self.filename:
            self._solution_type = 'top'
        elif '/all/' in self.filename:
            self._solution_type = 'regular'
        else:
            msg = 'IRData property error: solution type from filename="%s'
            logger.info(msg, self.filename)
            self._solution_type = None

        return self._solution_type

    @property
    def solution_id(self):
        if hasattr(self, '_solution_id'):
            return self._solution_id

        # want, have
        self._solution_id, sid_str = None, self._data.get('SID')

        if sid_str is None:
            msg = 'IRData property error: no solution id, filename="%s"'
            logger.info(msg, self.filename)
            return self._solution_id

        try:
            self._solution_id = int(sid_str)
        except ValueError:
            msg = 'IRData property error: SID is not an int: SID="%s"'
            logger.info(msg, sid_str, self.filename)

        return self._solution_id

    @property
    def puzzle_id(self):
        if hasattr(self, '_puzzle_id'):
            return self._puzzle_id

        # want, have
        self._puzzle_id, pid_str = (None, self._data.get('PID'))

        if pid_str is None:
            msg = 'IRData property error: no puzzle id: filename="%s"'
            logger.info(msg, self.filename)
            return self._puzzle_id

        try:
            self._puzzle_id = int(pid_str)
        except ValueError:
            msg = 'IRData property error: PID is not an int: PID="%s"'
            logger.info(msg, pid_str, self.filename)

        return self._puzzle_id

    @property
    def history_id(self):
        if hasattr(self, '_history_id'):
            return self._history_id

        # want, have
        self._history_id, history_string = (None, self._data.get('HISTORY'))

        if history_string is None:
            msg = 'IRData property error: solution has no history: filename="%s"'
            logger.info(msg, self.filename)
            return self._history_id

        # does not fail if history_string is a string
        last_move_in_history = history_string.split(',')[-1]
        try:
            self._history_id, _ = last_move_in_history.split(':')
        except ValueError:
            msg = 'IRData property error: unable to process history string: history_string="%s"'
            logger.info(msg, history_string)

        return self._history_id

    @property
    def moves(self):
        if hasattr(self, '_moves'):
            return self._moves

        self._moves = None

        if self.history_id is None:
            return self._moves

        history_string = self._data.get('HISTORY')
        try:
            moves = [int(pair.split(':')[1])
                     for pair in history_string.split(',')]
        except (IndexError, ValueError, TypeError):
            msg = 'IRData property error: unable to parse moves from history string: history_string="%s"'
            logger.info(msg, history_string)
        else:
            self._moves = sum(moves)

        return self._moves

    @property
    def score(self):
        if hasattr(self, '_score'):
            return self._score

        # want, have
        self._score, score_str = None, self._data.get('SCORE')

        if score_str is None:
            msg = 'IRData property error: missing score: filename="%s"'
            logger.info(msg, self.filename)
            return self._score

        try:
            self._score = float(score_str)
        except ValueError:
            msg = 'IRData property error: SCORE is not a float: score_str="%s"'
            logger.info(msg, score_str)

        return self._score

    def to_model_object(self, name):
        """Create a model object."""
        Model = getattr(tables, name)
        model = Model.from_irdata(self)
        return model

    def pdls(self):
        """Create PDL objects from PDL strings in the IRData."""
        # want, have
        pdls, pdl_strings = [], self._data['PDL']

        if not isinstance(pdl_strings, list):
            pdl_strings = [pdl_strings, ]

        for pdl_string in pdl_strings:
            try:
                pdl = PDL(pdl_string)
            except PDLCreationError as err:
                msg = 'PDL creation error: %s'
                logging.info(msg, err)
            else:
                pdls.append(pdl)

        return pdls


class PDL:
    def __init__(self, pdl_str):
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

        self._data = dict(
            player_name=player_name,
            team_name=team_name,
            player_id=player_id,
            team_id=team_id
        )

    @property
    def team_type(self):
        if self._data['team_name'] == '[no group]':
            team_type = 'soloist'
        else:
            team_type = 'evolver'
        return team_type

    def __getattr__(self, key):
        return self._data[key]

    def to_model_object(self, name):
        """Create a model object."""
        Model = getattr(tables, name)
        model = Model.from_pdl(self)
        return model
