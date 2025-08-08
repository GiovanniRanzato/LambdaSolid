import uuid
from unittest.mock import MagicMock

import pytest
from sqlalchemy import Column, String

from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.interfaces.DBObjectI import DBObjectI
from outputs.db.interfaces.DBTableI import DBTableI
from outputs.db.sql_db.ORM.BaseORM import Base
from outputs.db.sql_db.SqlDB import SqlDB
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI
from outputs.db.sql_db.tables.SqlDBTableBase import SqlDBTableBase


class DummyOrmClass(Base):
    __tablename__ = 'dummy_table'
    dummy_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    dummy_name = Column(String(50), nullable=False)


class DummyDBObject(DBObjectI):
    def __init__(self, dummy_id: str, dummy_name: str):
        self.dummy_id = dummy_id
        self.dummy_name = dummy_name

    def model_dump(self):
        return {"dummy_id": self.dummy_id, "dummy_name": self.dummy_name}

class TestSqlDBTableBase:
    @pytest.fixture
    def dummy_orm_object(self) -> DBObjectI:
        return DummyOrmClass()

    @pytest.fixture
    def dummy_db_object(self) -> DBObjectI:
        return DummyDBObject(dummy_id="dummy_id", dummy_name="dummy_name")

    @pytest.fixture
    def serializer(self):
        return MagicMock(spec=SqlORMSerializerI)

    @pytest.fixture
    def config(self):
        return MagicMock(spec=ConfigI)

    @pytest.fixture
    def parent_class(self):
        return MagicMock()

    @pytest.fixture
    def sql_db_table_base(self, monkeypatch, dummy_orm_object, dummy_db_object, serializer, config, parent_class):
        # Mock the call to SqlDBTableBase parents
        monkeypatch.setattr("outputs.db.sql_db.SqlDB.SqlDB.__init__", parent_class)

        return SqlDBTableBase(
            orm_class=dummy_orm_object.__class__,
            obj_class=dummy_db_object.__class__,
            serializer=serializer,
            config=config
        )

    def test_initialization(
            self, sql_db_table_base, dummy_orm_object, dummy_db_object, serializer, config, parent_class):
        assert isinstance(sql_db_table_base, DBTableI)
        assert isinstance(sql_db_table_base, SqlDB)

        # Check if the parent class was called
        parent_class.assert_called_once_with(config)

    def test_create(self, sql_db_table_base, dummy_orm_object, dummy_db_object, serializer):
        serializer.to_db.return_value = dummy_orm_object
        serializer.from_db.return_value = dummy_db_object

        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        result = sql_db_table_base.create(dummy_db_object)

        assert result == dummy_db_object
        serializer.to_db.assert_called_once_with(dummy_db_object, sql_db_table_base.orm_class)
        serializer.from_db.assert_called_once_with(dummy_orm_object, sql_db_table_base.obj_class)

        # check if the session was used correctly
        session_mock.add.assert_called_once_with(dummy_orm_object)
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once_with(dummy_orm_object)

    def test_update(self, sql_db_table_base, dummy_orm_object, dummy_db_object, serializer):
        serializer.to_db.return_value = dummy_orm_object
        serializer.from_db.return_value = dummy_db_object

        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        result = sql_db_table_base.update(dummy_db_object)

        assert result == dummy_db_object
        serializer.to_db.assert_called_once_with(dummy_db_object, sql_db_table_base.orm_class)
        serializer.from_db.assert_called_once_with(dummy_orm_object, sql_db_table_base.obj_class)

        # check if the session was used correctly
        session_mock.merge.assert_called_once_with(dummy_orm_object)
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once_with(dummy_orm_object)

    def test_get(self, sql_db_table_base, dummy_orm_object, dummy_db_object, serializer):
        serializer.from_db.return_value = dummy_db_object

        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        # Mock the get method to return the dummy ORM object
        session_mock.get.return_value = dummy_orm_object

        result = sql_db_table_base.get("dummy_id")

        assert result == dummy_db_object
        serializer.from_db.assert_called_once_with(dummy_orm_object, sql_db_table_base.obj_class)

    def test_get_not_found(self, sql_db_table_base):
        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        # Mock the get method to return None
        session_mock.get.return_value = None

        result = sql_db_table_base.get("non_existent_id")

        assert result is None

    def test_delete(self, sql_db_table_base, dummy_orm_object, serializer):
        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        # Mock the get method to return the dummy ORM object
        session_mock.get.return_value = dummy_orm_object

        result = sql_db_table_base.delete("dummy_id")

        assert result is True

        # check if the session was used correctly
        session_mock.delete.assert_called_once_with(dummy_orm_object)
        session_mock.commit.assert_called_once()
        session_mock.get.assert_called_once_with(sql_db_table_base.orm_class, "dummy_id")

    def test_delete_not_found(self, sql_db_table_base):
        # Mock the session_local context manager (with self.session_local() as session:)
        session_mock = MagicMock()
        session_mock.__enter__.return_value = session_mock
        session_mock.__exit__.return_value = None
        sql_db_table_base.session_local = MagicMock(return_value=session_mock)

        # Mock the get method to return None
        session_mock.get.return_value = None

        result = sql_db_table_base.delete("non_existent_id")

        assert not result









