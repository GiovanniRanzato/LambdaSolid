from infrastructure.interfaces.EventI import EventI
from infrastructure.interfaces.HandlerI import HandlerI
from infrastructure.EventsRegistry import EventsRegistry


class HandlerFactory:
    def __init__(self, events_registry: EventsRegistry):
        self.events_registry = events_registry

    def create_handler(self, event: EventI) -> HandlerI:
        handlers = self.events_registry.get_handlers_registry()
        event_type = event.get_event_type()

        handler_class = handlers.get(event_type)
        if handler_class is None:
            raise ValueError(f"No handler registered for event type: {event_type}")

        return handler_class()
