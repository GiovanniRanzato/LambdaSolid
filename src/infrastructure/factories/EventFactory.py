from infrastructure.interfaces.EventI import EventI
from infrastructure.EventsRegistry import EventsRegistry


class EventFactory:
    def __init__(self, events_registry: EventsRegistry):
        self.events_registry = events_registry

    def create_event(self, event_dict: dict, context: dict = None) -> "EventI":
        for registered_event in self.events_registry.get_events_registry().values():
            if registered_event.is_valid(event_dict):
                return registered_event.from_dict(event_dict, context)

        raise ValueError(f"Unknown event type: {event_dict}")
