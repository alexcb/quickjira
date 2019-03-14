import curses

class button(object):
    def __init__(self, text, callback):
        self.t = text
        self.callback = callback
        self.height = 1

    def get_state(self):
        return None

    def load_state(self, state):
        pass

    def handle_key(self, key):
        if key == 'KEY_ENTER':
            self.callback()

    def text(self):
        return self.t

    def draw(self, stdscr, y, x, selected):
        opts = []
        if selected:
            opts.append(curses.A_REVERSE)
        stdscr.addstr(y, x, self.text(), *opts)

    def draw_cursor(self, stdscr, y, x):
        curses.curs_set(0)
