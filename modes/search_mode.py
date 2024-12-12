from typing import Tuple

from interfaces.modes.base_mode import IMode
from MyString import MyString
from utils.keys import Keys


class SearchMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key: Keys | Tuple[Keys, str]) -> None:
        if key in [Keys.LEFT, Keys.RIGHT]:
            self.process_navigation_key(key)
        elif key == Keys.ESCAPE:
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.BACKSPACE:
            self.controller.search_model.delete_char_before_cursor()
        elif key == Keys.DELETE:
            self.controller.search_model.delete_char_after_cursor()
        elif key == Keys.ENTER:
            self.controller.text_model.find_matches(self.controller.search_model.get_search_text().c_str())
            if self.controller.search_model.is_reversed():
                self.controller.text_model.move_to_previous_match()
            else:
                self.controller.text_model.move_to_next_match()
            self.controller.set_mode(self.controller.text_mode)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.search_model.add_char(char)

    def process_navigation_key(self, key: Keys) -> None:
        if key == Keys.LEFT:
            self.controller.search_model.move_cursor(-1)
        elif key == Keys.RIGHT:
            self.controller.search_model.move_cursor(1)

    def enter(self) -> None:
        self.controller.search_model.clear()
        self.controller.search_view.display(self.controller.search_model)
        row, col = self.controller.search_model.get_cursor_position()
        self.controller.search_view.update_cursor(row, col)

    def update_view(self) -> None:
        self.controller.search_view.display(self.controller.search_model)
        row, col = self.controller.search_model.get_cursor_position()
        self.controller.search_view.update_cursor(row, col)
        pass

    def exit(self) -> None:
        self.controller.text_view.display_status("")
        pass
