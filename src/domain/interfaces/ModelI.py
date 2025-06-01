from abc import abstractmethod, ABC


class ModelI(ABC):
    @abstractmethod
    def model_dump_json(self) -> dict:
        """Returns a JSON representation of the model sample."""