from abc import ABC, abstractmethod


class DBObjectI(ABC):

    @abstractmethod
    def model_dump(self) -> dict:
        """Returns the object as a dictionary"""


