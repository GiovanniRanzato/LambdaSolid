from unittest.mock import MagicMock, call

import pytest

from infrastructure.App import App
from infrastructure.containers import Container
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.interfaces.HandlerI import HandlerI
from inputs.api_gateway.APIGatewayHandler import APIGatewayHandler
from inputs.api_gateway.events.APIGatewayEventV1 import APIGatewayEventV1
from inputs.sns.events.SNSEventSample import SNSEventSample
from inputs.sns.handlers.SNSEventSampleHandler import SNSEventHandlerSample


class TestApp:
    @pytest.fixture
    def events_registry(self) -> EventsRegistry:
        return MagicMock(spec=EventsRegistry)

    @pytest.fixture
    def event_factory(self) -> EventFactory:
        return MagicMock(spec=EventFactory)

    @pytest.fixture
    def app(self, events_registry, event_factory):
        events_registry.register_event = MagicMock(return_value=None)
        return App(event_factory=event_factory, events_registry=events_registry)

    def test_init(self, app, events_registry, event_factory):
        assert app.events_registry == events_registry
        assert app.event_factory == event_factory
        assert isinstance(app, App)

        events_registry.register_event.assert_has_calls(
            [call(APIGatewayEventV1, APIGatewayHandler), call(SNSEventSample, SNSEventHandlerSample)]
        )

    def test_run(self, app, event_factory, events_registry, mocker):
        event = {"key": "value"}
        context = {"context_key": "context_value"}

        parsed_event = MagicMock()
        event_factory.create_event.return_value = parsed_event

        # Simula il tipo di handler restituito dal registry
        handler_class = MagicMock()
        events_registry.resolve_handler_class.return_value = handler_class

        # Mock del container.wire
        container_mock = MagicMock(spec=Container)
        container_mock.wire = MagicMock()
        mocker.patch("infrastructure.App.Container", return_value=container_mock)

        # Mock dell'handler e della factory
        handler_instance = MagicMock(spec=HandlerI)
        handler_instance.handle.return_value = "response"

        factory_mock = MagicMock()
        factory_mock.return_value = handler_instance  # chiamando factory_mock() ottieni l'handler

        # Patcha providers.Factory per restituire factory_mock
        mocker.patch("infrastructure.App.providers.Factory", return_value=factory_mock)

        result = app.run(event, context)

        # Asserzioni
        event_factory.create_event.assert_called_once_with(event, context)
        events_registry.resolve_handler_class.assert_called_once_with(parsed_event)
        factory_mock.assert_called_once()  # controlla che la factory sia stata chiamata
        handler_instance.handle.assert_called_once_with(event=parsed_event)
        assert result == "response"
