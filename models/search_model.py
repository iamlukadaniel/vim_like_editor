from typing import Tuple
from MyString import MyString
from models.cursor_model import CursorModel
from interfaces.models import ISearchModel


class SearchModel(ISearchModel):
    def __init__(self):
        self.search_text: MyString = MyString()
        self.cursor: CursorModel = CursorModel()
        self.is_reversed_flag: bool = False
        self.is_dir_right_flag: bool = True

    def add_char(self, char: str) -> None:
        self.search_text.insert(self.cursor.col, char)
        self.move_cursor(1)

    def clear(self) -> None:
        self.search_text.clear()
        self.cursor.col = 0

    def delete_char_after_cursor(self) -> None:
        current_line = self.search_text
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)

    def delete_char_before_cursor(self) -> None:
        current_line = self.search_text
        if self.cursor.col > 0:
            self.move_cursor(-1)
            current_line.erase(self.cursor.col, 1)

    def move_cursor(self, col_offset: int) -> None:
        line_length = self.search_text.size()
        self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))

    def get_cursor_position(self) -> Tuple[int, int]:
        return self.cursor.get_position()

    def get_search_text(self) -> MyString:
        return self.search_text

    def is_reversed(self) -> bool:
        return self.is_reversed_flag

    def set_reversed(self, is_reversed: bool) -> None:
        self.is_reversed_flag = is_reversed

    def is_dir_right(self) -> bool:
        return self.is_dir_right_flag

    def set_dir_right(self, is_dir_right: bool) -> None:
        self.is_dir_right_flag = is_dir_right
