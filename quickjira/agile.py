import requests
from pprint import pprint

def get_current_sprint(url, user, password, board_id):
    r = requests.get(f'{url}/rest/agile/1.0/board/{board_id}/sprint?state=active', auth=(user, password))
    values = r.json()['values']
    if len(values) != 1:
        raise RuntimeError(f'expected exactly one sprint; got {len(values)}')
    return values[0]['id']
