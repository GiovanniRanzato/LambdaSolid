import json

from infrastructure.interfaces.EventI import EventI


class SNSEventBase(EventI):
    def __init__(self, event: dict):
        self.event = event

    @classmethod
    def get_event_type(cls) -> str:
        return cls.__name__

    @classmethod
    def from_dict(cls, event: dict, context: dict | None) -> "SNSEventBase":
        if not cls.is_valid(event):
            raise ValueError(f"Invalid event format for SNSEventBase: {event}")

        return cls(event=event)

    @staticmethod
    def _get_content(event: dict) -> dict:
        return json.loads(event.get("Sns").get("Message"))

    @classmethod
    def is_valid(cls, event: dict) -> bool:
        if event.get("EventSource") != "aws:sns" or event.get("Sns", {}).get("Message") is None:
            return False

        return cls._get_content(event).get("type") == cls.get_event_type()

