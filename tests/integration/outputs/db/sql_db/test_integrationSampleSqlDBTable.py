import datetime
import uuid

import pytest

from domain.models.ModelSample import ModelSample
from infrastructure import depends
from infrastructure.containers import Container
from outputs.db.sql_db.tables.SqlDBTableSample import SqlDBTableSample
from outputs.db.interfaces.DBTableI import DBTableI


class TestIntegrationSampleSqlDBTable:
    @pytest.fixture
    def container(self):
        container = Container()
        container.wire(modules=[__name__])
        yield container
        container.unwire()

    @pytest.fixture
    def db_table_sample(self) -> DBTableI:
        return depends.get_sql_db_table_sample()

    @pytest.fixture
    def sample_model(self):
        return ModelSample(
            sample_id=uuid.uuid4().hex,
            name="Test Sample",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    def test_init(self, db_table_sample):
        assert isinstance(db_table_sample, SqlDBTableSample)

    def test_create(self, db_table_sample, sample_model):
        sample_model.sample_id = None
        sample_model.created_at = None
        sample_model.updated_at = None
        result = db_table_sample.create(sample_model)
        assert getattr(result, "sample_id") is not None

        retrieved_model = db_table_sample.get(getattr(result, "sample_id"))

        assert getattr(retrieved_model, "name") == sample_model.name

    def test_get_item(self, db_table_sample, sample_model):
        created_item = db_table_sample.create(sample_model)

        retrieved_model = db_table_sample.get(sample_model.sample_id)

        assert retrieved_model is not None
        assert isinstance(retrieved_model, ModelSample)
        assert retrieved_model.sample_id == created_item.sample_id
        assert retrieved_model.name == sample_model.name
        assert retrieved_model.name == created_item.name
