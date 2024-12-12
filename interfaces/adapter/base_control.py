from abc import ABC, abstractmethod
from typing import Tuple
from utils.keys import Keys


class IControl(ABC):
    @abstractmethod
    def get_key(self) -> Keys | Tuple[Keys, str]:
        pass
