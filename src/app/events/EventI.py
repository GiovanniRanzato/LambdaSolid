from abc import ABC, abstractmethod


class EventI(ABC):
    @classmethod
    @abstractmethod
    def get_event_type(cls) -> str:
        """Get the event type"""

    @classmethod
    @abstractmethod
    def from_dict(cls, event: dict, context: dict | None) -> "EventI":
        """Create an event from a dictionary"""

    @classmethod
    @abstractmethod
    def is_valid(cls, event: dict) -> bool:
        """Check if the event is valid"""
