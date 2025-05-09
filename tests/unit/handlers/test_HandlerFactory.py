from unittest.mock import MagicMock

import pytest

from app.events.EventI import EventI
from app.events.EventsRegistry import EventsRegistry
from app.handlers.HandlerFactory import HandlerFactory
from app.handlers.HandlerI import HandlerI


class DummyHandler(HandlerI):
    def handle(self, event):
        pass


class TestHandlerFactory:
    @pytest.fixture
    def events_registry(self):
        return MagicMock(spec=EventsRegistry)

    @pytest.fixture
    def handler_factory(self, events_registry):
        return HandlerFactory(events_registry=events_registry)

    def test_init(self, handler_factory, events_registry):
        assert isinstance(handler_factory, HandlerFactory)
        assert handler_factory.events_registry == events_registry

    def test_create_handler_returns_correct_handler(self, handler_factory, events_registry):
        # Prepare
        event = MagicMock(spec=EventI)
        event.get_event_type.return_value = event_type = "TestEvent"

        events_registry.get_handlers_registry.return_value = {event_type: DummyHandler}

        # Execute
        handler = handler_factory.create_handler(event)

        # Assert
        assert isinstance(handler, DummyHandler)

    def test_create_handler_raises_for_unknown_event(self, handler_factory, events_registry):
        # Arrange
        event = MagicMock(spec=EventI)
        event.get_event_type.return_value = "UnknownEvent"

        events_registry.get_handlers_registry.return_value = {}

        # Act & Assert
        with pytest.raises(ValueError, match="No handler registered for event type: UnknownEvent"):
            handler_factory.create_handler(event)
