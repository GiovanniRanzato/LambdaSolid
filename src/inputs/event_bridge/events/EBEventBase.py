from infrastructure.interfaces.EventI import EventI


class EBEventBase(EventI):
    def __init__(self, event: dict):
        if not self.is_valid(event):
            raise ValueError(f"Invalid event format for EBEventBase: {event}")
        self.event = event

    @classmethod
    def get_event_type(cls) -> str:
        return cls.__name__

    @classmethod
    def from_dict(cls, event: dict, context: dict | None) -> "EBEventBase":
        if not cls.is_valid(event):
            raise ValueError(f"Invalid event format for EBEventBase: {event}")

        return cls(event=event)

    @classmethod
    def is_valid(cls, event: dict) -> bool:
        if (
            event.get("source", None) != "aws.events"
            or event.get("resources", None) is None
            or not isinstance(event.get("resources"), list)
            or event.get("resources")[0] != "arn:aws:events:rule/{}".format(cls.get_event_type())
        ):
            return False
        return True
