import requests
from pprint import pprint

def get_current_sprint(url, user, password, board_id):
    r = requests.get(f'{url}/rest/agile/1.0/board/{board_id}/sprint?state=active', auth=(user, password))
    values = r.json()['values']

    # pick the right sprint
    values = [x for x in values if 'Time Series' in x['name']]

    if len(values) != 1:
        print(values)
        raise RuntimeError(f'expected exactly one sprint in board {board_id}; got {values}')
    return values[0]['id']
