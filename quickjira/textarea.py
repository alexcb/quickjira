import curses

class textarea(object):
    def __init__(self):
        self.t = [[]]
        self.cursor_x = 0
        self.cursor_y = 0
        self.height = 10

    def value(self):
        s = ''
        for row in self.t:
            s = s + '\n' + ''.join(row)
        return s

    def get_state(self):
        return self.value()

    def load_state(self, state):
        self.t = [list(x) for x in state.split('\n')]

    def handle_key(self, key):
        row = self.t[self.cursor_y] 
        on_end = len(row) == self.cursor_x

        if key == 'KEY_BACKSPACE':
            if self.cursor_x > 0:
                row = row[:self.cursor_x-1] + row[self.cursor_x:]
                self.t[self.cursor_y] = row
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                #join lines
                prev = self.t[self.cursor_y-1]
                curr = self.t[self.cursor_y]
                self.t[self.cursor_y-1] = prev + curr
                del self.t[self.cursor_y]
                self.cursor_y -= 1
                self.cursor_x = len(prev)
        elif key == 'KEY_DC':
            if self.cursor_x < len(row):
                row = row[:self.cursor_x] + row[(self.cursor_x+1):]
                self.t[self.cursor_y] = row
            elif self.cursor_y < len(self.t)-1:
                # join lines
                curr = self.t[self.cursor_y]
                next_line = self.t[self.cursor_y+1]
                self.t[self.cursor_y] = curr + next_line
                del self.t[self.cursor_y+1]
        elif key == 'KEY_UP':
            if self.cursor_y > 0:
                self.cursor_y -= 1
                if on_end:
                    self.cursor_x = len(self.t[self.cursor_y])
                else:
                    self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
        elif key == 'KEY_DOWN':
            if self.cursor_y < (len(self.t)-1):
                self.cursor_y += 1
                self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
                if on_end:
                    self.cursor_x = len(self.t[self.cursor_y])
                else:
                    self.cursor_x = min(self.cursor_x, len(self.t[self.cursor_y]))
        elif key == 'KEY_LEFT':
            if self.cursor_x > 0:
                self.cursor_x -= 1
        elif key == 'KEY_RIGHT':
            if self.cursor_y < len(self.t):
                if self.cursor_x < len(self.t[self.cursor_y]):
                    self.cursor_x += 1
        elif key == 'KEY_ENTER':
            before_cursor = row[:self.cursor_x]
            after_cursor = row[self.cursor_x:]
            self.t[self.cursor_y] = before_cursor
            self.cursor_y += 1
            self.cursor_x = 0
            self.t = self.t[:self.cursor_y] + [after_cursor] + self.t[self.cursor_y:]
        else:
            if len(key) == 1:
                if self.cursor_y == len(self.t):
                    self.t.append([])
                row = row[:self.cursor_x] + [key] + row[self.cursor_x:]
                self.t[self.cursor_y] = row
                self.cursor_x += 1

    def draw(self, stdscr, y, x, selected):
        i = 0
        j = len(self.t)

        if j > self.height:
            i = max(self.cursor_y - int(self.height/2), 0)
            j = i + self.height + 1

        self.relative_cursor_y = self.cursor_y - i

        while i < j and i < len(self.t):
            row = self.t[i]
            s = ''.join(row)
            stdscr.addstr(y, x, s)
            i += 1
            y += 1

    def draw_cursor(self, stdscr, y, x):
        curses.curs_set(1)
        x += self.cursor_x
        y += self.relative_cursor_y
        stdscr.addstr(y, x, '')


