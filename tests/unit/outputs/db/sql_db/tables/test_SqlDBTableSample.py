from unittest.mock import MagicMock

import pytest

from domain.models.ModelSample import ModelSample
from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.sql_db.ORM.SampleORM import SampleORM
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI
from outputs.db.sql_db.tables.SqlDBTableSample import SqlDBTableSample
class TestSqlDBTableSample:
    @pytest.fixture
    def sql_orm_serializer(self) -> SqlORMSerializerI:
        return MagicMock(spec=SqlORMSerializerI)

    @pytest.fixture
    def config(self) -> ConfigI:
        return MagicMock(spec=ConfigI)

    def test_initialize(self, sql_orm_serializer, config, monkeypatch):
        # Mock the parent class initialization to check if it is called correctly
        parent_class = MagicMock()
        monkeypatch.setattr("outputs.db.sql_db.tables.SqlDBTableBase.SqlDBTableBase.__init__", parent_class)

        sql_db_sample_table = SqlDBTableSample(serializer=sql_orm_serializer, config=config)
        assert isinstance(sql_db_sample_table, SqlDBTableSample)

        # Check if the parent class was called with the correct parameters
        parent_class.assert_called_once_with(
            orm_class=SampleORM,
            obj_class=ModelSample,
            serializer=sql_orm_serializer,
            config=config)
