from MyString import MyString
from models.cursor_model import CursorModel


class SearchModel:
    def __init__(self):
        self.search_text = MyString()  # Текст для поиска
        self.cursor = CursorModel()  # Экземпляр курсора для строки поиска
        self.is_reversed = False
        self.is_dir_right = True

    def add_char(self, char: str):
        self.search_text += char
        self.move_cursor(1)

    def clear(self):
        self.search_text.clear()
        self.cursor.col = 0

    def delete_char_after_cursor(self):
        current_line = self.search_text
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)

    def delete_char_before_cursor(self):
        current_line = self.search_text
        if self.cursor.col > 0:
            self.move_cursor(-1)
            current_line.erase(self.cursor.col, 1)

    def move_cursor(self, col_offset: int):
        line_length = self.search_text.size()
        self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))
