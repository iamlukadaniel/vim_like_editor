from abc import ABC, abstractmethod


class IControl(ABC):
    @abstractmethod
    def get_key(self):
        pass
