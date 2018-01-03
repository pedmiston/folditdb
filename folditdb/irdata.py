import json

from folditdb import tables

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
        self._pdl = None

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data)

    @classmethod
    def from_file(cls, json_filepath):
        with open(json_filepath) as f:
            return cls.from_json(f.read())

    @property
    def filename(self):
        return self._data['FILEPATH']

    @property
    def solution_id(self):
        return int(self._data['SID'])

    @property
    def puzzle_id(self):
        return int(self._data['PID'])

    @property
    def history_id(self):
        if 'HISTORY' not in self._data:
            raise InvalidSolutionError
        return self._data['HISTORY'].split(',')[-1].split(':')[0]

    @property
    def score(self):
        if 'SCORE' not in self._data:
            raise InvalidSolutionError
        score = self._data['SCORE']
        try:
            score = float(score)
        except ValueError:
            raise InvalidSolutionError
        return score

    def to_model_object(self, name):
        """Create a model object."""
        Model = getattr(tables, name)
        model = Model.from_irdata(self)
        return model

    def pdl_strings(self):
        pdls = self._data['PDL']
        if not isinstance(pdls, list):
            pdls = [pdls, ]
        return pdls


class InvalidSolutionError(Exception):
    """Something's not right with this solution."""
