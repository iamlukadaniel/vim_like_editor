import curses
from adapter.interface_tui import ITUI
from adapter.interface_control import IControl
from utils.keys import Keys


class CursesAdapter(ITUI, IControl):
    def __init__(self):
        self.screen = curses.initscr()
        self.key_map = {}
        self._initialize_key_map()

    def _initialize_key_map(self):
        self.key_map = {
            curses.KEY_EXIT: Keys.ESCAPE,
            curses.KEY_ENTER: Keys.ENTER,
            curses.KEY_BACKSPACE: Keys.BACKSPACE,
            curses.KEY_DC: Keys.DELETE,
            curses.KEY_UP: Keys.UP,
            curses.KEY_DOWN: Keys.DOWN,
            curses.KEY_LEFT: Keys.LEFT,
            curses.KEY_RIGHT: Keys.RIGHT,
            9: Keys.TAB,
            27: Keys.ESCAPE,  # ESC key
            ord('\n'): Keys.ENTER,
        }

        for code in range(32, 127):
            char = chr(code)
            self.key_map[code] = (Keys.CHAR, char)

    def init(self):
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(1)
        curses.meta(True)
        curses.set_escdelay(25)

    def cleanup(self):
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()

    def get_key(self):
        key = self.screen.getch()
        return self._map_key(key)

    def _map_key(self, key):
        mapped_key = self.key_map.get(key, None)
        return mapped_key

    def draw(self, y: int, x: int, text: str):
        try:
            self.screen.addstr(y, x, text)
        except curses.error:
            pass

    def refresh(self):
        self.screen.refresh()

    def clear(self):
        self.screen.clear()

    def move_cursor(self, y: int, x: int):
        self.screen.move(y, x)

    def get_screen_size(self):
        return self.screen.getmaxyx()
