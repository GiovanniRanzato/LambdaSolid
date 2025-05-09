from unittest.mock import MagicMock

import pytest
from app.App import App
from app.events.EventFactory import EventFactory
from app.events.EventsRegistry import EventsRegistry
from app.handlers.HandlerFactory import HandlerFactory


class TestApp:
    @pytest.fixture
    def events_registry(self) -> EventsRegistry:
        return MagicMock(spec=EventsRegistry)

    @pytest.fixture
    def event_factory(self) -> EventFactory:
        return MagicMock(spec=EventFactory)

    @pytest.fixture
    def event_handler_factory(self) -> HandlerFactory:
        return MagicMock(spec=HandlerFactory)

    @pytest.fixture
    def app(self, events_registry, event_factory, event_handler_factory):
        events_registry.register_event = MagicMock()
        return App(event_factory=event_factory, handler_factory=event_handler_factory, events_registry=events_registry)

    def test_init(self, app, events_registry, event_factory, event_handler_factory):
        assert app.events_registry == events_registry
        assert app.event_factory == event_factory
        assert app.handler_factory == event_handler_factory
        assert isinstance(app, App)

        # Check if the events_registry has been called to register events
        # events_registry.register_event.assert_called_once_with(APIGatewayEvent, APIGatewayHandler)

    def test_run(self, app, event_factory, event_handler_factory):
        event = {"key": "value"}
        context = {"context_key": "context_value"}

        parsed_event = MagicMock()
        event_factory.create_event.return_value = parsed_event

        handler = MagicMock()
        event_handler_factory.create_handler.return_value = handler

        app.run(event, context)

        event_factory.create_event.assert_called_once_with(event, context)
        event_handler_factory.create_handler.assert_called_once_with(parsed_event)
        handler.handle.assert_called_once_with(event=parsed_event)
