from abc import ABC, abstractmethod


class EBEventSampleI(ABC):
    @abstractmethod
    def get_event_sample_name(self) -> str:
        """Return the name of the event sample"""
