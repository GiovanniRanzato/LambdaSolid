from typing import Type

from infrastructure.interfaces.EventI import EventI
from infrastructure.interfaces.HandlerI import HandlerI


class EventsRegistry:
    _events_registry = {}
    _handlers_registry = {}

    @classmethod
    def register_event(cls, event_class: Type[EventI], event_handler_class: Type[HandlerI]):
        cls._events_registry[event_class.__name__] = event_class
        cls._handlers_registry[event_class.__name__] = event_handler_class

    def get_events_registry(self) -> {str, Type[EventI]}:
        return self._events_registry

    def resolve_handler_class(self, event: EventI) -> Type[HandlerI]:
        event_type = event.get_event_type()
        handler_class = self._handlers_registry.get(event_type)
        if handler_class is None:
            raise ValueError(f"No handler registered for event type: {event_type}")
        return handler_class
