import pytest
from infrastructure.containers import Container
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.factories.EventFactory import EventFactory


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

    def test_event_registry(self, container, registry):
        assert isinstance(registry, EventsRegistry)

    def test_event_factory(self, container, event_factory, registry):
        assert isinstance(event_factory, EventFactory)
        assert event_factory.events_registry is registry
