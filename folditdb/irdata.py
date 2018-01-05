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
            raise IRDataCreationError('bad JSON: {e}'.format(e=err))
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
            msg = 'IRData property error: solution type from {}'
            logger.info(msg.format(self.filename))
            self._solution_type = None

        return self._solution_type

    @property
    def solution_id(self):
        if hasattr(self, '_solution_id'):
            return self._solution_id

        error_msg = 'IRData property error: coverting SID to int'
        self._solution_id = self.verify_int(self._data.get('SID'),
                                            error_msg=error_msg)
        return self._solution_id

    @property
    def puzzle_id(self):
        if hasattr(self, '_puzzle_id'):
            return self._puzzle_id

        error_msg = 'IRData property error: converting PID to int'
        self._puzzle_id = self.verify_int(self._data.get('PID'),
                                          error_msg=error_msg)
        return self._puzzle_id

    @property
    def history_id(self):
        if hasattr(self, '_history_id'):
            return self._history_id

        history_string = self._data.get('HISTORY')
        if history_string is None:
            msg = 'IRData property error: solution has no history: filename={}'
            logger.info(msg.format(self.filename))
            return None

        # does not fail if history_string is a string
        last_move_in_history = history_string.split(',')[-1]
        try:
            history_id, _ = last_move_in_history.split(':')
        except ValueError:
            msg = 'IRData property error: unable to process history string: {}'
            logger.info(msg.format(history_string))

        self._history_id = history_id
        return self._history_id

    @property
    def moves(self):
        if hasattr(self, '_moves'):
            return self._moves

        if self.history_id is None:
            self._moves = None
            return self._moves

        history_string = self._data.get('HISTORY')
        try:
            moves = [int(pair.split(':')[1])
                     for pair in history_string.split(',')]
        except (IndexError, ValueError, TypeError):
            msg = 'IRData property error: unable to parse moves from history string: {}'
            logger.info(msg.format(history_string))
            self._moves = None
        else:
            self._moves = sum(moves)

        return self._moves

    @property
    def score(self):
        if hasattr(self, '_score'):
            return self._score

        score_str = self._data.get('SCORE')
        if score_str is None:
            logger.info('IRData property error: missing score')
            self._score = None
            return self._score

        try:
            self._score = float(score_str)
        except ValueError:
            msg = 'IRData property error: converting score_str to float: score_str="{}""'
            logger.info(msg.format(score_str))
            self._score = None

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
                msg = 'error creating PDL from string="{}": {}'
                logging.info(msg.format(pdl_string, err))
            else:
                pdls.append(pdl)

        return pdls

    def verify_int(self, arg, error_msg):
        try:
            arg_int = int(arg)
        except (ValueError, TypeError):
            logger.info('{error_msg}: {arg}'.format(error_msg=error_msg, arg=arg))
            return None
        else:
            return arg_int


class PDL:
    def __init__(self, pdl_str):
        if pdl_str.startswith('. '):
            pdl_str = pdl_str.strip('^. ')
        else:
            msg = 'PDL string does not look right: {}'
            raise PDLCreationError(msg.format(pdl_str))

        fields = pdl_str.split(',')
        player_name, team_name = fields[:2]
        try:
            player_id, team_id = map(int, fields[2:4])
        except ValueError:
            msg = 'unable to convert player_id and team_id to ints'
            raise PDLCreationError(msg)

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
