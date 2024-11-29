from MyString import MyString
from models.cursor_model import CursorModel


# TODO: 1. Перенести execute_command по соответствующим режимам
#       2. Дополнить нужными методами
class CommandModel:
    def __init__(self):
        self.cursor = CursorModel()
        self.command_text = MyString()

    def add_char(self, char: str):
        self.command_text += char
        self.move_cursor(1)

    def clear(self):
        self.command_text.clear()
        self.cursor.col = 0

    def delete_char_after_cursor(self):
        current_line = self.command_text
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)

    def delete_char_before_cursor(self):
        current_line = self.command_text
        if self.cursor.col > 0:
            self.move_cursor(-1)
            current_line.erase(self.cursor.col, 1)

    def move_cursor(self, col_offset: int):
        line_length = self.command_text.size()
        self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))
