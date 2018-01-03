from folditdb import tables

class PDL:
    def __init__(self, pdl_str):
        fields = pdl_str.split(',')
        self._data = dict(
            player_name=fields[0].strip('^. '),
            team_name=fields[1],
            player_id=int(fields[2]),
            team_id=int(fields[3])
        )

    @property
    def player_name(self):
        return self._data['player_name']

    @property
    def team_name(self):
        return self._data['team_name']

    @property
    def player_id(self):
        return self._data['player_id']

    @property
    def team_id(self):
        return self._data['team_id']

    def to_model_object(self, name):
        """Create a model object."""
        Model = getattr(tables, name)
        model = Model.from_pdl(self)
        return model
