from typing import Tuple

from interfaces.modes.base_mode import IMode
from utils.keys import Keys


class InputMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key: Keys | Tuple[Keys, str]) -> None:
        if key == Keys.ESCAPE:
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.controller.text_model.insert_text('\n')
        elif key == Keys.BACKSPACE:
            self.controller.text_model.delete_char_before_cursor()
        elif key == Keys.DELETE:
            self.controller.text_model.delete_char_after_cursor()
        elif key == Keys.TAB:
            self.controller.text_model.insert_text('    ')
        elif key == Keys.DOWN:
            self.controller.text_model.move_cursor_input(1, 0)
        elif key == Keys.UP:
            self.controller.text_model.move_cursor_input(-1, 0)
        elif key == Keys.LEFT:
            self.controller.text_model.move_cursor_input(0, -1)
        elif key == Keys.RIGHT:
            self.controller.text_model.move_cursor_input(0, 1)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.text_model.insert_text(char)

    def enter(self) -> None:
        self.update_view()

    def update_view(self) -> None:
        self.controller.text_view.display(self.controller.text_model)
        self.controller.text_view.display_status("-- INSERT --")
        row, col = self.controller.text_model.get_cursor_position()
        self.controller.text_view.update_cursor(row, col)

    def exit(self) -> None:
        self.controller.text_view.display_status("")
