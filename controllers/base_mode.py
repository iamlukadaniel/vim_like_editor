from abc import ABC, abstractmethod


class IMode(ABC):
    @abstractmethod
    def handle_input(self, key):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def update_view(self):
        pass

    @abstractmethod
    def exit(self):
        pass
