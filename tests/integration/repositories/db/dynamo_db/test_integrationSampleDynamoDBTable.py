import datetime
import uuid
from dataclasses import dataclass

import pytest

from domain.models.ModelSample import ModelSample
from infrastructure import depends
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
    def db_table_sample(self) -> DBTableI:
        return depends.get_db_table_sample()

    @pytest.fixture
    def sample_model(self):
        return ModelSample(
            sample_id=uuid.uuid4().hex,
            name="Test Sample",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    def test_init(self, db_table_sample):
        assert isinstance(db_table_sample, DynamoDBTableSample)

    def test_create(self, db_table_sample, sample_model):
        sample_model.sample_id = ""
        result = db_table_sample.create(sample_model)
        assert getattr(result, 'sample_id') is not None

        retrieved_model = db_table_sample.get(getattr(result, 'sample_id'))

        assert getattr(retrieved_model, 'name') == sample_model.name

    def test_nested_db_object(self, db_table_sample, sample_model):
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
        sample_model = DummySampleModel(sample_id=uuid.uuid4().hex, nested_prop=nested_object)

        sample_model.sample_id = ""
        result = db_table_sample.create(sample_model)
        assert result.sample_id is not None

        retrieved_dict = db_table_sample.table.get_item(Key={db_table_sample.pk: sample_model.sample_id})

        assert retrieved_dict["Item"]["nested_prop"]["prop"] == nested_object.prop
        db_table_sample.obj_class = DummySampleModel
        retrieved_object = db_table_sample.get(sample_model.sample_id)

        assert retrieved_object.nested_prop.prop == nested_object.prop
        assert isinstance(retrieved_object, DummySampleModel)
        assert isinstance(retrieved_object.nested_prop, DummyNestedModel)

    def test_get_item(self, db_table_sample, sample_model):
        created_item = db_table_sample.create(sample_model)

        retrieved_model = db_table_sample.get(sample_model.sample_id)

        assert retrieved_model is not None
        assert isinstance(retrieved_model, ModelSample)
        assert retrieved_model.sample_id == created_item.sample_id
        assert retrieved_model.name == sample_model.name
        assert retrieved_model.name == created_item.name
