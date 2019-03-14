import requests
import json

from .agile import get_current_sprint


SPRINT_FIELD       = 'customfield_10004'
STORY_POINTS_FIELD = 'customfield_10008'

def create_issue(url, username, password, project, board_id, summary, description, estimate, active_sprint, assignee):
    if not isinstance(estimate, int):
        raise ValueError('estimate')

    data = {
        'fields': {
            'project':
            {
                'key': project,
            },
            'summary': summary,
            'description': description,
            'issuetype': {
                'name': 'Story'
            },       
            STORY_POINTS_FIELD: estimate,
        }
    }

    if active_sprint:
        sprint_id = get_current_sprint(url, username, password, board_id)
        data['fields'][SPRINT_FIELD] = sprint_id

    if assignee:
        data['fields']['assignee'] = {'name': assignee}


    headers = {
        'Content-Type': 'application/json',
    }
    r = requests.post(f'{url}/rest/api/2/issue/', headers=headers, auth=(username, password), data=json.dumps(data))
    r.raise_for_status()
    res = r.json()
    return res['key']

