from abc import abstractmethod, ABC


class ModelI(ABC):
    @abstractmethod
    def json(self) -> dict:
        """Returns a JSON representation of the model sample."""