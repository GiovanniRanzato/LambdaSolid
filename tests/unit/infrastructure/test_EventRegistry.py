from typing import Type
from unittest.mock import MagicMock

import pytest

from infrastructure.interfaces.EventI import EventI
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.interfaces.HandlerI import HandlerI


class TestEventRegistry:
    @pytest.fixture
    def event_registry(self):
        return EventsRegistry()

    @pytest.fixture
    def dummy_event(self):
        class DummyEvent(EventI):
            @classmethod
            def get_event_type(cls):
                return cls.__name__

            @classmethod
            def from_dict(cls, event: dict, context: dict | None) -> "EventI":
                return cls()

            @classmethod
            def is_valid(cls, event: dict) -> bool:
                return True

        return DummyEvent()

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

    def test_resolve_handler_class(self, event_registry, dummy_event):
        handler_type = Type[HandlerI]
        event_registry.register_event(type(dummy_event), handler_type)

        result = event_registry.resolve_handler_class(dummy_event)

        assert result == handler_type

    def test_cant_handler_class(self, event_registry, dummy_event):
        handler_type = Type[HandlerI]
        event_registry.register_event(type(dummy_event), handler_type)
        not_registered_event = MagicMock(spec=EventI)

        with pytest.raises(ValueError, match="No handler registered for event type:"):
            event_registry.resolve_handler_class(not_registered_event)
