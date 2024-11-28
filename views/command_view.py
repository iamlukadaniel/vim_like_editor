from adapter.interface_tui import ITUI
from models.command_model import CommandModel


class CommandView:
    def __init__(self, tui: ITUI):
        self.tui = tui

    def display(self, model: CommandModel):
        max_y, max_x = self.tui.get_screen_size()
        command_line = f":{model.command_text.c_str()}"
        self.tui.draw(max_y - 1, 0, command_line.ljust(max_x))
        self.tui.refresh()

    def update_cursor(self, line: int, col: int):
        max_y, max_x = self.tui.get_screen_size()
        self.tui.move_cursor(max_y - 1, col + 1)
