from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDBTableBase import DynamoDBTableBase
from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBSerializerI import DBSerializerI


class TestDynamoDBTableBase:
    @pytest.fixture
    def config(self) -> ConfigI:
        config = MagicMock(spec=ConfigI)
        config.get.side_effect = lambda key: {
            "DYNAMODB_REGION": "eu-west-1",
            "LOCALSTACK_ENDPOINT_URL": "http://localhost:4566",
        }.get(key, None)
        return config

    @pytest.fixture
    def table(self):
        mock = MagicMock()
        mock.name = "test_table"
        return mock

    @pytest.fixture
    def serializer(self):
        return MagicMock(spec=DBSerializerI)

    @pytest.fixture
    def db_obj(self):
        @dataclass
        class DummyDBObjClass(DBObjectI):
            id: str = None
            attr: str = "test_value"

            def model_dump(self) -> dict:
                return self.__dict__

        return DummyDBObjClass()

    @pytest.fixture
    def boto3_resource(self, table):
        mock = MagicMock()
        mock.Table.return_value = table
        return mock

    @pytest.fixture
    def boto3_client(self):
        mock = MagicMock()
        return mock

    @pytest.fixture
    def dynamo_db_table_base(self, config, serializer, db_obj, boto3_resource, boto3_client, mocker):
        mocker.patch("repositories.db.dynamo_db.DynamoDB.boto3.resource", return_value=boto3_resource)
        mocker.patch("repositories.db.dynamo_db.DynamoDB.boto3.client", return_value=boto3_client)
        return DynamoDBTableBase(
            table_name="test_table", pk="id", obj_class=db_obj.__class__, serializer=serializer, config=config
        )

    def test_init(self, dynamo_db_table_base, db_obj, config, serializer, boto3_resource, table):
        assert isinstance(dynamo_db_table_base, DynamoDBTableBase)
        assert dynamo_db_table_base.pk == "id"
        assert dynamo_db_table_base.obj_class == db_obj.__class__
        assert dynamo_db_table_base.serializer == serializer
        assert dynamo_db_table_base.table == table
        boto3_resource.Table.assert_called_once_with("test_table")

    def test_create(self, dynamo_db_table_base, db_obj, serializer, table):
        serializer.to_db.return_value = expected_dict = {"id": "12345", "attr": "test_value"}

        result = dynamo_db_table_base.create(db_object=db_obj)

        assert getattr(result, "id") is not None
        serializer.to_db.assert_called_once_with(db_obj)
        table.put_item.assert_called_once_with(Item=expected_dict)

    def test_update(self, dynamo_db_table_base, db_obj, serializer, table):
        db_obj.id = "12345"
        serializer.to_db.return_value = expected_dict = {"id": "12345", "attr": "test_value"}

        result = dynamo_db_table_base.update(db_object=db_obj)

        serializer.to_db.assert_called_once_with(db_obj)
        table.put_item.assert_called_once_with(Item=expected_dict)
        assert result == db_obj

    def test_get(self, dynamo_db_table_base, db_obj, serializer, table):
        table.get_item.return_value = returned_dict = {"Item": {"id": "12345", "attr": "test_value"}}
        serializer.from_db.return_value = db_obj

        result = dynamo_db_table_base.get("12345")

        serializer.from_db.assert_called_once_with(data=returned_dict["Item"], obj_class=db_obj.__class__)
        table.get_item.assert_called_once_with(Key={dynamo_db_table_base.pk: "12345"})
        assert result == db_obj

    def test_get_not_return_item(self, dynamo_db_table_base, db_obj, serializer, table):
        table.get_item.return_value = {"a_unexpected_key": "some_value"}
        serializer.from_db.return_value = db_obj

        result = dynamo_db_table_base.get("12345")

        table.get_item.assert_called_once_with(Key={dynamo_db_table_base.pk: "12345"})
        serializer.from_db.assert_not_called()

        assert result is None

    def test_delete(self, dynamo_db_table_base, db_obj, serializer, boto3_client, table):
        boto3_client.delete_item.return_value = True

        result = dynamo_db_table_base.delete("12345")

        boto3_client.delete_item.assert_called_once_with(
            TableName=table.name, Key={dynamo_db_table_base.pk: {"S": "12345"}}
        )
        assert result is True
