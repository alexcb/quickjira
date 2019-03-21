import curses

class textarea(object):
    def __init__(self):
        self.t = []
        self.height = None
        self.width = None
        self.cursor = 0
        self.cursor_map = None

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
            while self.cursor > 0:
                if self.cursor > 0 and self.t[self.cursor-1] == '\n':
                    break
                self.cursor -= 1
        elif key == 'KEY_END':
            while self.cursor < len(self.t):
                if self.cursor < len(self.t)-1 and self.t[self.cursor+1] == '\n':
                    break
                self.cursor += 1
        elif key == 'KEY_DOWN':
            x, y = self.get_cursor()
            if y < len(self.cursor_map) - 1:
                self.cursor = self.cursor_map[y+1]
                while x > 0:
                    if self.cursor >= len(self.t):
                        break
                    if self.t[self.cursor] == '\n':
                        break
                    self.cursor += 1
                    x -= 1
        elif key == 'KEY_UP':
            x, y = self.get_cursor()
            if y > 0:
                self.cursor = self.cursor_map[y-1] + x
        elif key == 'KEY_ENTER':
            self.t = self.t[:self.cursor] + ['\n'] + self.t[self.cursor:]
            self.cursor += 1
        else:
            if len(key) == 1:
                self.t = self.t[:self.cursor] + [key] + self.t[self.cursor:]
                self.cursor += 1
        #elif key == 'KEY_UP':
        #    if self.cursor_y > 0:
        #        self.cursor_y -= 1
        #        if on_end:
        #            self.cursor_x = len(self.t[self.cursor_y])
        #        else:
        #            self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
        #elif key == 'KEY_DOWN':
        #    if self.cursor_y < (len(self.t)-1):
        #        self.cursor_y += 1
        #        self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
        #        if on_end:
        #            self.cursor_x = len(self.t[self.cursor_y])
        #        else:
        #            self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
        #elif key == 'KEY_ENTER':
        #    before_cursor = row[:self.cursor_x]
        #    after_cursor = row[self.cursor_x:]
        #    self.t[self.cursor_y] = before_cursor
        #    self.cursor_y += 1
        #    self.cursor_x = 0
        #    self.t = self.t[:self.cursor_y] + [after_cursor] + self.t[self.cursor_y:]

    def draw(self, stdscr, y, x, selected):
        top_line = 0
        l = 0
        start = 0
        self.cursor_map = []

        i = 0
        while 1:
            if i >= len(self.t):
                break
            c = self.t[i]
            s = None
            if i - start == self.width:
                j = i
                next_start = j
                word_split = False
                if self.t[j-1] != ' ' and self.t[j] != ' ':
                    # we split a word in half!
                    split_ok = True
                    while self.t[j-1] != ' ':
                        if j == (start+1):
                            split_ok = False
                            break
                        j -= 1
                        next_start = j
                    if split_ok == False:
                        j = i
                        next_start = j

                s = ''.join(self.t[start:j])
                if '\n' in s:
                    raise ValueError((s, self.t, start, j))
                self.cursor_map.append(start)
                start = next_start
                i = j
            elif c == '\n':
                s = ''.join(self.t[start:i])
                self.cursor_map.append(start)
                start = i+1
                assert '\n' not in s
                i += 1
            else:
                i += 1

            if s is not None:
                if top_line <= l:
                    yy = l - top_line
                    stdscr.addstr(y+yy, x, s)
                l += 1

        s = ''.join(self.t[start:])
        assert '\n' not in s
        self.cursor_map.append(start)
        if s:
            if top_line <= l:
                yy = l - top_line
                stdscr.addstr(y+yy, x, s)
            l += 1

    def draw_cursor(self, stdscr, y, x):
        xx, yy = self.get_cursor()
        x += xx
        y += yy
        curses.curs_set(1)
        stdscr.addstr(y, x, '')


    def get_cursor(self):
        i = len(self.cursor_map)-1
        while i > 0:
            if self.cursor >= self.cursor_map[i]:
                break
            i -= 1
        x = self.cursor - self.cursor_map[i]
        return (x, i)
