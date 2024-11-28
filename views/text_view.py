from adapter.interface_tui import ITUI
from models.text_model import TextModel


class TextView:
    def __init__(self, tui: ITUI):
        self.tui = tui

    def display(self, model: TextModel):
        self.tui.clear()
        max_y, max_x = self.tui.get_screen_size()
        for i, line in enumerate(model.lines):
            if i >= max_y - 2:  # Leave space for status line
                break
            display_text = line.c_str()
            if len(display_text) > max_x:
                display_text = display_text[:max_x]
            self.tui.draw(i, 0, display_text)
        self.tui.refresh()

    def update_cursor(self, line: int, col: int):
        self.tui.move_cursor(line, col)

    def display_status(self, status: str):
        max_y, max_x = self.tui.get_screen_size()
        self.tui.draw(max_y - 1, 0, status.ljust(max_x))
        self.tui.refresh()
