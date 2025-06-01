from unittest.mock import MagicMock

import pytest

from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.interfaces.ConfigI import ConfigI
from infrastructure.depends import get_config, get_events_registry, get_events_factory, get_dynamo_db_serializer, \
    get_db_table_sample
from repositories.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.interfaces.DBSerializerI import DBSerializerI
from repositories.interfaces.DBTableI import DBTableI


class TestDepends:
    @pytest.fixture
    def config(self):
        return MagicMock(spec=ConfigI)

    @pytest.fixture
    def config_mock(self, config, mocker):
        return mocker.patch("infrastructure.depends.Config", return_value=config)

    @pytest.fixture
    def event_registry(self):
        return MagicMock(spec=EventsRegistry)

    @pytest.fixture
    def event_registry_mock(self, event_registry, mocker):
        return mocker.patch("infrastructure.depends.EventsRegistry", return_value=event_registry)

    @pytest.fixture
    def dynamo_db_serializer(self):
        return MagicMock(spec=DynamoDBSerializer)

    @pytest.fixture
    def dynamo_db_serializer_mock(self, dynamo_db_serializer, mocker):
        return mocker.patch("infrastructure.depends.DynamoDBSerializer", return_value=dynamo_db_serializer)

    def test_get_config(self):
        result = get_config()
        assert isinstance(result, ConfigI)

    def test_get_event_registry(self):
        result = get_events_registry()
        assert isinstance(result, EventsRegistry)

    def test_get_event_factory(self, event_registry_mock, event_registry):
        result = get_events_factory()
        assert isinstance(result, EventFactory)
        assert result.events_registry == event_registry
        event_registry_mock.assert_called_once()

    def test_get_dynamo_db_serializer(self):
        result = get_dynamo_db_serializer()
        assert isinstance(result, DynamoDBSerializer)
        assert isinstance(result, DBSerializerI)

    def test_get_db_table_sample(self, dynamo_db_serializer_mock, dynamo_db_serializer, config_mock, config):
        config.get.side_effect = lambda key: {
            "DYNAMODB_REGION": "eu-west-1",
            "LOCALSTACK_ENDPOINT_URL": "http://localhost:4566",
            "DYNAMODB_SAMPLE_TABLE": "test_table_sample",
            "DYNAMODB_SAMPLE_TABLE_PK": "sample_id",
        }.get(key)

        result = get_db_table_sample()
        assert isinstance(result, DynamoDBTableSample)
        assert isinstance(result, DBTableI)
        dynamo_db_serializer_mock.assert_called_once()
        config_mock.assert_called_once()
