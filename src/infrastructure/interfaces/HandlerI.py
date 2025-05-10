from abc import ABC, abstractmethod

from infrastructure.interfaces.EventI import EventI


class HandlerI(ABC):
    @abstractmethod
    def handle(self, event: EventI):
        """Handle an event"""
