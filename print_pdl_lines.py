import json

for json_str in open('1506601828.json'):
    data = json.loads(json_str)
    if 'PDL' in data:
        if not isinstance(data['PDL'], list):
            data['PDL'] = [data['PDL'], ]
        for i, pdl in enumerate(data['PDL']):
            print(i, ':', pdl.split(',')[:4])
    else:
        print('PDL not in solution data')
