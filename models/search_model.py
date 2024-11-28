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
        self.cursor.col += 1

    def clear(self):
        self.search_text.clear()
        self.cursor.col = 0




