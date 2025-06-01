from unittest.mock import MagicMock

import pytest

from domain.services.ServiceSample import ServiceSample
from infrastructure.containers import Container
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.db.interfaces.DBSerializerI import DBSerializerI
from repositories.db.interfaces.DBTableI import DBTableI


class TestContainers:
    @pytest.fixture
    def container(mocker) -> Container:
        container = Container()
        # Override config per evitare chiamate reali ad AWS
        mock_config = MagicMock(spec=ConfigI)
        container.config.override(mock_config)
        return container

    @pytest.fixture
    def registry(self, container) -> EventsRegistry:
        return container.events_registry()

    @pytest.fixture
    def event_factory(self, container) -> EventFactory:
        return container.event_factory()

    @pytest.fixture
    def dynamo_db_serializer(self, container) -> DBSerializerI:
        return container.dynamo_db_serializer()

    @pytest.fixture
    def db_table_sample(self, container) -> DBTableI:
        mock_config = MagicMock(spec=ConfigI)
        mock_config.get.side_effect = lambda key: {
            "DYNAMODB_REGION": "eu-west-1",
            "LOCALSTACK_ENDPOINT_URL": "http://localhost:4566",
            "DYNAMODB_SAMPLE_TABLE": "test_table_sample",
            "DYNAMODB_SAMPLE_TABLE_PK": "sample_id",
        }.get(key)

        container.config.override(mock_config)
        return container.db_table_sample()

    @pytest.fixture
    def service_sample(self, container) -> ServiceSample:
        db_table_sample = MagicMock(spec=DynamoDBTableSample)
        container.db_table_sample.override(db_table_sample)
        return container.service_sample()

    def test_event_registry(self, container, registry):
        assert isinstance(registry, EventsRegistry)

    def test_event_factory(self, container, event_factory, registry):
        assert isinstance(event_factory, EventFactory)
        assert event_factory.events_registry is registry

