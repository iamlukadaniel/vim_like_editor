from abc import ABC, abstractmethod


class ITUI(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def draw(self, y: int, x: int, text: str):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def move_cursor(self, y: int, x: int):
        pass

    @abstractmethod
    def get_screen_size(self):
        pass
