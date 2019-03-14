import curses

class toggle(object):
    def __init__(self, choices, initial_index=0):
        self.choices = choices
        self.i = initial_index
        self.height = 1

    def value(self):
        return self.choices[self.i]

    def get_state(self):
        return self.i

    def load_state(self, state):
        self.i = state

    def handle_key(self, key):
        if key in ('KEY_ENTER', ' '):
            self.i += 1
            if self.i >= len(self.choices):
                self.i = 0

    def text(self):
        return self.choices[self.i]

    def draw(self, stdscr, y, x, selected):
        opts = []
        if selected:
            opts.append(curses.A_REVERSE)
        stdscr.addstr(y, x, self.text(), *opts)

    def draw_cursor(self, stdscr, y, x):
        curses.curs_set(0)

