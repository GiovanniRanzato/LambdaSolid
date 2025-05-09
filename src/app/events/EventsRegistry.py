from typing import Type

from app.events.EventI import EventI
from app.handlers.HandlerI import HandlerI


class EventsRegistry:
    _events_registry = {}
    _handlers_registry = {}

    @classmethod
    def register_event(cls, event_class: Type[EventI], event_handler_class: Type[HandlerI]):

        cls._events_registry[event_class.__name__] = event_class
        cls._handlers_registry[event_class.__name__] = event_handler_class

    def get_events_registry(self) ->  {str, Type[EventI]}:
        return self._events_registry

    def get_handlers_registry(self) ->  {str, Type[HandlerI]}:
        return self._handlers_registry

