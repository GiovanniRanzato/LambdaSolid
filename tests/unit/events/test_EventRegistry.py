from typing import Type

import pytest

from infrastructure.interfaces.EventI import EventI
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.interfaces.HandlerI import HandlerI


class TestEventRegistry:
    @pytest.fixture
    def event_registry(self):
        return EventsRegistry()

    def test_init(self, event_registry):
        assert isinstance(event_registry, EventsRegistry)
        assert event_registry._events_registry == {}
        assert event_registry._handlers_registry == {}

    def test_register_event(self, event_registry):
        event_type = Type[EventI]
        handler_type = Type[HandlerI]

        event_registry.register_event(event_type, handler_type)

        assert event_registry._events_registry[event_type.__name__] == event_type
        assert event_registry._handlers_registry[event_type.__name__] == handler_type

    def test_get_events_registry(self, event_registry):
        event_type = Type[EventI]
        handler_type = Type[HandlerI]
        event_registry.register_event(event_type, handler_type)

        events_registry = event_registry.get_events_registry()

        assert events_registry == {event_type.__name__: event_type}

    def test_get_handlers_registry(self, event_registry):
        event_type = Type[EventI]
        handler_type = Type[HandlerI]
        event_registry.register_event(event_type, handler_type)

        handlers_registry = event_registry.get_handlers_registry()

        assert handlers_registry == {event_type.__name__: handler_type}
