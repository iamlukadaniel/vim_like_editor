from typing import Tuple

from MyString import MyString
from models.cursor_model import CursorModel
from interfaces.models import ICommandModel


class CommandModel(ICommandModel):
    def __init__(self):
        self.cursor: CursorModel = CursorModel()
        self.command_text: MyString = MyString()
        self.current_file: MyString = MyString()
        self.command_count: int | None = None
        self.awaiting_arg_for: str | None = None

    def get_command_count(self) -> int | None:
        return self.command_count

    def set_command_count(self, command_count: int | None) -> None:
        self.command_count = command_count

    def get_awaiting_argument_for(self) -> str | None:
        return self.awaiting_arg_for

    def set_awaiting_argument_for(self, awaiting_arg_for: str | None) -> None:
        self.awaiting_arg_for = awaiting_arg_for

    def get_command_text(self) -> MyString:
        return self.command_text

    def get_current_file(self) -> MyString:
        return self.current_file

    def set_current_file(self, filename: str) -> None:
        self.current_file = MyString(filename)

    def add_char(self, char: str) -> None:
        self.command_text.insert(self.cursor.col, char)
        self.move_cursor(1)

    def clear(self) -> None:
        self.command_text.clear()
        self.cursor.col = 0

    def delete_char_after_cursor(self) -> None:
        current_line = self.command_text
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)

    def delete_char_before_cursor(self) -> None:
        current_line = self.command_text
        if self.cursor.col > 0:
            self.move_cursor(-1)
            current_line.erase(self.cursor.col, 1)

    def move_cursor(self, col_offset: int) -> None:
        line_length = self.command_text.size()
        self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))

    def get_cursor_position(self) -> Tuple[int, int]:
        return self.cursor.row, self.cursor.col
