from abc import ABC, abstractmethod


class IMode(ABC):
    @abstractmethod
    def handle_input(self, key) -> None:
        pass

    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def update_view(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass
