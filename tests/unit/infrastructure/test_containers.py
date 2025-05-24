import pytest

from domain.services.ServiceSample import ServiceSample
from infrastructure.containers import Container
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.factories.EventFactory import EventFactory
from repositories.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.interfaces.DBSerializerI import DBSerializerI
from repositories.interfaces.DBTableI import DBTableI


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

    def test_db_serializer(self, container):
        db_serializer = container.db_serializer()
        assert db_serializer is not None
        assert isinstance(db_serializer, DBSerializerI)
        assert hasattr(db_serializer, 'to_db')
        assert hasattr(db_serializer, 'from_db')

    def test_db_table_sample(self, container):
        db_table_sample = container.db_table_sample()
        assert db_table_sample is not None
        assert isinstance(db_table_sample, DynamoDBTableSample)
        assert isinstance(db_table_sample, DBTableI)
        assert hasattr(db_table_sample, 'create')
        assert hasattr(db_table_sample, 'get')
        assert hasattr(db_table_sample, 'update')
        assert hasattr(db_table_sample, 'delete')

    def test_service_sample(self, container):
        service_sample = container.service_sample()
        assert isinstance(service_sample, ServiceSample)
        assert service_sample is not None
        assert hasattr(service_sample, 'sample_db_table')

