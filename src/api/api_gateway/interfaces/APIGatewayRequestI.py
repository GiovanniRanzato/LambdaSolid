from abc import abstractmethod

from infrastructure.interfaces.EventI import EventI


class APIGatewayRequestI(EventI):
    @abstractmethod
    def get_body(self) -> dict:
        """Get the body of the event"""

    @abstractmethod
    def get_context(self):
        """Get the context of the event"""

    @abstractmethod
    def get_stage(self) -> str:
        """Get the stage of the event"""

    @abstractmethod
    def get_version(self) -> str:
        """Get the stage of the event"""