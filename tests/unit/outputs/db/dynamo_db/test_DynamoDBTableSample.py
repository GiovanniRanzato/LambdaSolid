from unittest.mock import MagicMock

import pytest

from outputs.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample


class TestDynamoDBTableSample:
    @pytest.fixture
    def config(self):
        config = MagicMock()
        config.get.side_effect = lambda key: {
            "DYNAMODB_REGION": "eu-west-1",
            "LOCALSTACK_ENDPOINT_URL": "http://localhost:4566",
            "DYNAMODB_SAMPLE_TABLE": "test_table_sample",
            "DYNAMODB_SAMPLE_TABLE_PK": "sample_id",
        }.get(key, None)
        return config

    @pytest.fixture
    def serializer(self):
        return MagicMock()

    @pytest.fixture
    def dynamo_db_table_sample(self, config, serializer):
        return DynamoDBTableSample(config=config, serializer=serializer)

    def test_init(self, dynamo_db_table_sample, config):
        assert isinstance(dynamo_db_table_sample, DynamoDBTableSample)
        assert dynamo_db_table_sample.table.name == "test_table_sample"
        assert dynamo_db_table_sample.pk == "sample_id"
        assert dynamo_db_table_sample.table.name == "test_table_sample"
