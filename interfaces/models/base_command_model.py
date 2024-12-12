from abc import ABC, abstractmethod
from MyString import MyString
from typing import Tuple, Optional


class ICommandModel(ABC):
    @abstractmethod
    def add_char(self, char: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def get_command_text(self) -> MyString:
        pass

    @abstractmethod
    def move_cursor(self, col_offset: int) -> None:
        pass

    @abstractmethod
    def delete_char_before_cursor(self) -> None:
        pass

    @abstractmethod
    def delete_char_after_cursor(self) -> None:
        pass

    @abstractmethod
    def get_command_count(self) -> int | None:
        pass

    @abstractmethod
    def set_command_count(self, command_count: int | None) -> None:
        pass

    @abstractmethod
    def get_awaiting_argument_for(self) -> str | None:
        pass

    @abstractmethod
    def set_awaiting_argument_for(self, awaiting_arg_for: str | None) -> None:
        pass

    @abstractmethod
    def get_current_file(self) -> str:
        pass

    @abstractmethod
    def set_current_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def get_cursor_position(self) -> Tuple[int, int]:
        pass
