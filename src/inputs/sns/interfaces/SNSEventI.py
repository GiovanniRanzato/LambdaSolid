from abc import ABC, abstractmethod
from typing import Any


class SNSEventI(ABC):
    @abstractmethod
    def get_content(self) -> dict:
        """Returns the content of the SNS event."""