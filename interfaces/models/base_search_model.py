from abc import ABC, abstractmethod
from typing import Tuple


class ISearchModel(ABC):
    @abstractmethod
    def add_char(self, char: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def delete_char_before_cursor(self) -> None:
        pass

    @abstractmethod
    def delete_char_after_cursor(self) -> None:
        pass

    @abstractmethod
    def move_cursor(self, col_offset: int) -> None:
        pass

    @abstractmethod
    def get_cursor_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_search_text(self) -> str:
        pass

    @abstractmethod
    def is_reversed(self) -> bool:
        pass

    @abstractmethod
    def set_reversed(self, is_reversed: bool) -> None:
        pass

    @abstractmethod
    def is_dir_right(self) -> bool:
        pass

    @abstractmethod
    def set_dir_right(self, is_dir_right: bool) -> None:
        pass

