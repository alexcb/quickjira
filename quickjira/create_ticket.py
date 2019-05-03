import requests
import json

from .agile import get_current_sprint


SPRINT_FIELD       = 'customfield_10004'
STORY_POINTS_FIELD = 'customfield_10008'

# To get these fields, the easiest way is to fetch an existing ticket; e.g.


def create_issue(url, username, password, project, board_id, summary, description, estimate, active_sprint, assignee):
    if not isinstance(estimate, int):
        raise ValueError('estimate')

    ##########################################3
    # DEBUGGING HELP
    #
    # update the ticket with one that shows the correct fields one needs,
    # then enable this code to get a full dump of the data.
    # 
    #ticket = 'PROJECT-1234'
    #get_url = f'{url}/rest/api/2/issue/{ticket}'
    #r = requests.get(get_url, auth=(username, password))
    #with open('/tmp/fuckjira', 'w') as fp:
    #    fp.write(r.text)
    #with open('/tmp/fuckjira.meta', 'w') as fp:
    #    fp.write(get_url)
    ##########################################3


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
    post_url = f'{url}/rest/api/2/issue/'
    json_data = json.dumps(data)
    r = requests.post(post_url, headers=headers, auth=(username, password), data=json_data)
    if r.status_code // 100 != 2:
        raise RuntimeError(f'failed to post to {post_url} with data {json_data}; status: {r.status_code}')
    res = r.json()
    return res['key']

