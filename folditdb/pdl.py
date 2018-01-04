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

        team_type = 'soloist' if self._data['team_name'] == '[no group]' else 'evolver'
        self._data['team_type'] = team_type

    def __getattr__(self, key):
        return self._data[key]

    def to_model_object(self, name):
        """Create a model object."""
        Model = getattr(tables, name)
        model = Model.from_pdl(self)
        return model
