from app.events.EventI import EventI


class APIGatewayEvent(EventI):
    def __init__(self, event: dict, context: dict | None):
        self.event = event
        self.context = context

    @classmethod
    def get_event_type(cls) -> str:
        return cls.__name__

    @classmethod
    def from_dict(cls, event: dict, context: dict | None) -> "APIGatewayEvent":
        if not cls.is_valid(event):
            raise ValueError(f"Invalid event format for APIGatewayEvent: {event}")

        return cls(event=event, context=context)

    @classmethod
    def is_valid(cls, event: dict) -> bool:
        return "routeKey" in event and "requestContext" in event
