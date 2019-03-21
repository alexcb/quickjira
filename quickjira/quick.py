import curses
import json
import os.path
import pathlib
import yaml
import subprocess
from contextlib import suppress

from .text import text
from .textarea import textarea
from .toggle import toggle
from .button import button

from .create_ticket import create_issue

quick_jira_bkup_path = '/tmp/.quickjira'

def get_config(path):
    with open(path, 'r') as fp:
        config = yaml.load(fp.read())

    # hacky checks to ensure all config options are present
    assert config['url'].startswith('https://')
    config['username']
    config['password']
    config['project']
    config['board_id']

    return config

def determine_widget_heights(widgets, max_height):
    num_variable = sum(1 for (_, _, height) in widgets if height == '*')
    known_height = sum(height for (_, _, height) in widgets if height != '*')
    var_height = None
    if num_variable > 0:
        var_height = (max_height - known_height) // num_variable
    heights = []
    for (_, _, height) in widgets:
        if height == '*':
            height = var_height
        heights.append(height)
    return heights


def main(stdscr, config):

    new_ticket_key = {
    }

    def on_submit():
        summary       = widgets[0][1].value()
        days          = widgets[1][1].value()
        active_sprint = widgets[2][1].value() == 'Y'
        assign_to_me  = widgets[3][1].value() == 'Y'
        description   = widgets[4][1].value()

        days = int(days)

        if assign_to_me:
            assignee = config['username']
        else:
            assignee = None

        issue_key = create_issue(
                config['url'],
                config['username'],
                config['password'],
                config['project'],
                config['board_id'],
                summary, description, days, active_sprint, assignee)

        url = f'{config["url"]}/browse/{issue_key}'
        subprocess.check_call(['/usr/bin/xdg-open', url])

        new_ticket_key['key'] = issue_key
    

    active_widget = 0
    widgets = [
            ('       summary: ', text(), 1),
            ('estimated days: ', text(), 1),
            (' active sprint: ', toggle(('Y', 'N'), initial_index=1), 1),
            ('  assign to me: ', toggle(('Y', 'N'), initial_index=1), 1),
            ('   description: ', textarea(), '*'),
            ('                ', button('<submit ticket>', on_submit), 1),
            ]

    # attempt restore
    with suppress(Exception):
        with open('/tmp/.quickjira', 'r') as fp:
            states = json.loads(fp.read())
        for label, widget, _ in widgets:
            if label in states:
                widget.load_state(states[label])

    def keep_running():
        return 'key' not in new_ticket_key

    try:
        while(keep_running()):
            stdscr.clear()
            height,width = stdscr.getmaxyx()
            heights = determine_widget_heights(widgets, height)

            cursor_loc = None
            y = 0
            for i, (label, widget, _) in enumerate(widgets):
                n = len(label)
                widget.width = width - n - 1 # leave an extra empty space for the cursor
                widget.height = heights[i] # leave an extra empty space for the cursor
                selected = bool(active_widget == i)

                stdscr.addstr(y, 0, f'{label}')
                widget.draw(stdscr, y, n, selected)
                y += widget.height

            if cursor_loc:
                y, x = cursor_loc
                stdscr.addstr(y, x, '')

            w = widgets[active_widget]
            x = len(w[0])
            y = active_widget
            w[1].draw_cursor(stdscr, y, x)

            stdscr.refresh()
            key = stdscr.getkey()
            if key == '\n':
                key = 'KEY_ENTER'
            elif key == '\t':
                key = 'KEY_TAB'

            if key == 'KEY_TAB':
                active_widget += 1
                if active_widget >= len(widgets):
                    active_widget = 0
            elif key == 'KEY_BTAB':
                active_widget -= 1
                if active_widget < 0:
                    active_widget = len(widgets) - 1

            widgets[active_widget][1].handle_key(key)
    except:
        states = {}
        for _, (label, widget, _) in enumerate(widgets):
            states[label] = widget.get_state()

        with open(quick_jira_bkup_path, 'w') as fp:
            fp.write(json.dumps(states))
        raise
    else:
        os.unlink(quick_jira_bkup_path)

def run():
    config = get_config(os.path.expanduser('~/.quickjira'))
    curses.wrapper(main, config)
