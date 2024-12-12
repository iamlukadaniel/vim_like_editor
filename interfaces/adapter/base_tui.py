from abc import ABC, abstractmethod
from typing import Tuple


class ITUI(ABC):
    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def draw(self, y: int, x: int, text: str) -> None:
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def move_cursor(self, y: int, x: int) -> None:
        pass

    @abstractmethod
    def get_screen_size(self) -> Tuple[int, int]:
        pass
