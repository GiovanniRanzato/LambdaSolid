from unittest.mock import MagicMock

import pytest

from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.dynamo_db.DynamoDB import DynamoDB


class TestDynamoDB:
    @pytest.fixture
    def config(self) -> ConfigI:
        config = MagicMock(spec=ConfigI)
        config.get.side_effect = lambda key: {
            "DYNAMODB_REGION": "eu-west-1",
            "LOCALSTACK_ENDPOINT_URL": "http://localhost:4566",
        }.get(key, None)
        return config

    @pytest.fixture
    def dynamo_db(self, config):
        return DynamoDB(config)

    def test_init(self, dynamo_db):
        assert dynamo_db.resource is not None
        assert dynamo_db.resource.meta.client._endpoint.host == "http://localhost:4566"
        assert dynamo_db.resource.meta.client.meta.region_name == "eu-west-1"
        assert isinstance(dynamo_db, DynamoDB)
