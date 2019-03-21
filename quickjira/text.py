import curses

class text(object):
    def __init__(self):
        self.t = []
        self.cursor = 0
        self.cursor_relative = 0
        self.height = None
        self.width = None

    def get_state(self):
        return ''.join(self.t)

    def value(self):
        return ''.join(self.t)

    def load_state(self, state):
        self.t = list(state)
        self.cursor = len(self.t)

    def handle_key(self, key):
        if key == 'KEY_BACKSPACE':
            if self.cursor > 0:
                self.t = self.t[:self.cursor-1] + self.t[self.cursor:]
                self.cursor -= 1
        elif key == 'KEY_DC':
            if self.cursor < len(self.t):
                self.t = self.t[:self.cursor] + self.t[(self.cursor+1):]
        elif key == 'KEY_LEFT':
            if self.cursor > 0:
                self.cursor -= 1
        elif key == 'KEY_RIGHT':
            if self.cursor < len(self.t):
                self.cursor += 1
        elif key == 'KEY_HOME':
            self.cursor = 0
        elif key == 'KEY_END':
            self.cursor = len(self.t)
        else:
            if len(key) == 1:
                self.t = self.t[:self.cursor] + [key] + self.t[self.cursor:]
                self.cursor += 1

    def text(self):
        if len(self.t) <= self.width:
            self.cursor_relative = self.cursor
            return ''.join(self.t)

        j = max(self.cursor, self.width)
        i = j - self.width
        s = ''.join(self.t[i:j])
        assert( len(s) == self.width)
        self.cursor_relative = self.cursor-i
        return s

    def draw(self, stdscr, y, x, selected):
        stdscr.addstr(y, x, self.text())

    def draw_cursor(self, stdscr, y, x):
        curses.curs_set(1)
        x += self.cursor_relative
        stdscr.addstr(y, x, '')

