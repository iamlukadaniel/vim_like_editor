from abc import ABC, abstractmethod
from MyString import MyString
from typing import Tuple


class ITextModel(ABC):
    @abstractmethod
    def get_lines(self) -> list[MyString]:
        pass

    @abstractmethod
    def get_line(self, line: int) -> MyString:
        pass

    @abstractmethod
    def copy_line(self) -> bool:
        pass

    @abstractmethod
    def copy_word(self) -> bool:
        pass

    @abstractmethod
    def paste_word(self) -> None:
        pass

    @abstractmethod
    def paste_line(self) -> None:
        pass

    @abstractmethod
    def find_matches(self, text: str) -> None:
        pass

    @abstractmethod
    def move_to_next_match(self) -> None:
        pass

    @abstractmethod
    def move_to_previous_match(self) -> None:
        pass

    @abstractmethod
    def insert_empty_line(self) -> None:
        pass

    @abstractmethod
    def erase_line(self) -> None:
        pass

    @abstractmethod
    def move_cursor(self, row_offset: int, col_offset: int) -> None:
        pass

    @abstractmethod
    def move_cursor_input(self, row_offset: int, col_offset: int) -> None:
        pass

    @abstractmethod
    def insert_text(self, text: str) -> None:
        pass

    @abstractmethod
    def delete_char_after_cursor(self) -> None:
        pass

    @abstractmethod
    def delete_char_before_cursor(self) -> None:
        pass

    @abstractmethod
    def get_cursor_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def set_cursor_position(self, row: int, col: int) -> None:
        pass

    @abstractmethod
    def go_to_line_start(self) -> None:
        pass

    @abstractmethod
    def go_to_line_end(self) -> None:
        pass

    @abstractmethod
    def go_to_file_start(self) -> None:
        pass

    @abstractmethod
    def go_to_file_end(self) -> None:
        pass

    @abstractmethod
    def go_to_next_word_end(self) -> None:
        pass

    @abstractmethod
    def go_to_prev_word_start(self) -> None:
        pass

    @abstractmethod
    def delete_word_under_cursor(self) -> None:
        pass

    @abstractmethod
    def go_to_line_n(self, n: int) -> None:
        pass

    @abstractmethod
    def save_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def load_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def is_modified(self) -> bool:
        pass
