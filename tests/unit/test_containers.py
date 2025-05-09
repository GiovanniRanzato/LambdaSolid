import pytest
from containers import Container
from app.events.EventsRegistry import EventsRegistry
from app.events.EventFactory import EventFactory
from app.events.handlers.HandlerFactory import HandlerFactory

class TestContainers:
    @pytest.fixture
    def container(self) -> Container:
        return Container()

    @pytest.fixture
    def registry(self, container) -> EventsRegistry:
        return container.events_registry()

    @pytest.fixture
    def event_factory(self, container) -> EventFactory:
        return container.event_factory()

    @pytest.fixture
    def event_handler_factory(self, container) -> HandlerFactory:
        return container.handler_factory()

    def test_event_registry(self, container, registry):
        assert isinstance(registry, EventsRegistry)

    def test_event_factory(self, container, event_factory, registry):
        assert isinstance(event_factory, EventFactory)
        assert event_factory.event_registry is registry

    def test_event_handler_factory(self, container, event_handler_factory, registry):
        assert isinstance(event_handler_factory, HandlerFactory)
        assert event_handler_factory.event_registry is registry
