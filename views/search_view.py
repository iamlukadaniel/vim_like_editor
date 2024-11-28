from adapter.interface_tui import ITUI
from models.search_model import SearchModel


class SearchView:
    def __init__(self, tui: ITUI):
        self.tui = tui

    def display(self, model: SearchModel):
        max_y, max_x = self.tui.get_screen_size()
        search_line = f"{'/' if model.is_dir_right else '?'}{model.search_text.c_str()}"
        self.tui.draw(max_y - 1, 0, search_line.ljust(max_x))
        self.tui.refresh()

    def update_cursor(self, line: int, col: int):
        max_y, max_x = self.tui.get_screen_size()
        self.tui.move_cursor(max_y - 1, col + 1)
