from abc import ABC, abstractmethod

from app.events.EventI import EventI


class HandlerI(ABC):
    @abstractmethod
    def handle(self, event: EventI):
        """Handle an event"""