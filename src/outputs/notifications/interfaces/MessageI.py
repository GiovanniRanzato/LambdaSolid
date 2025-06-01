from abc import abstractmethod, ABC


class MessageI(ABC):
    @abstractmethod
    def __str__(self):
        """Returns a string representation of the message."""