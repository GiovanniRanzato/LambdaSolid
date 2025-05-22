import datetime
import uuid
from dataclasses import dataclass

import pytest
from dependency_injector.wiring import Provide, inject

from domain.models.SampleModel import SampleModel
from infrastructure.containers import Container
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBTableI import DBTableI


class TestIntegrationSampleDynamoDBTable:
    @pytest.fixture
    def container(self):
        container = Container()
        container.wire(modules=[__name__])
        yield container
        container.unwire()

    @pytest.fixture
    @inject
    def sample_db_table(self, container: Container, sample_db_table=Provide[Container.sample_db_table]):
        return sample_db_table

    @pytest.fixture
    def sample_model(self):
        return SampleModel(
            sample_id=uuid.uuid4().hex,
            name="Test Sample",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_init(self, sample_db_table):
        assert isinstance(sample_db_table, DynamoDBTableSample)

    def test_save(self, sample_db_table, sample_model):
        result = sample_db_table.save(sample_model)
        assert result is True

        retrieved_model = sample_db_table.table.get_item(
            Key={sample_db_table.pk: sample_model.sample_id})

        assert retrieved_model['Item']['name'] == sample_model.name

    def test_nested_db_object(self, sample_db_table, sample_model):
        @dataclass
        class DummyNestedModel(DBObjectI):
            prop: str

            def model_dump(self) -> dict:
                return self.__dict__
        @dataclass
        class DummySampleModel:
            sample_id: str
            nested_prop: DummyNestedModel

            def model_dump(self) -> dict:
                return self.__dict__

        nested_object = DummyNestedModel(prop="nested_value")
        sample_model = DummySampleModel(
            sample_id=uuid.uuid4().hex,
            nested_prop=nested_object
        )

        result = sample_db_table.save(sample_model)
        assert result is True

        retrieved_dict = sample_db_table.table.get_item(
            Key={sample_db_table.pk: sample_model.sample_id})

        assert retrieved_dict['Item']['nested_prop']['prop'] == nested_object.prop
        sample_db_table.obj_class = DummySampleModel
        retrieved_object = sample_db_table.get(sample_model.sample_id)

        assert retrieved_object.nested_prop.prop == nested_object.prop
        assert isinstance(retrieved_object, DummySampleModel)
        assert isinstance(retrieved_object.nested_prop, DummyNestedModel)
