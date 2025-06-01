from abc import ABC, abstractmethod


class NotificationI(ABC):
    @abstractmethod
    def publish(self, message: str) -> None:
        """Publishes a message to the queue"""
