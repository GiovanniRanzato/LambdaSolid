from dataclasses import dataclass

import pytest

from repositories.db.DBObjectBase import DBObjectBase


class TestDBObject:
    @pytest.fixture
    def db_object(self):
        @dataclass
        class DummyDBObject(DBObjectBase):
            id: str
            name: str

        return DummyDBObject(id="123", name="Test")

    def test_init(self, db_object):
        assert db_object.id == "123"
        assert db_object.name == "Test"
        assert isinstance(db_object, DBObjectBase)

    def test_model_dump(self, db_object):
        expected_dict = {"id": "123", "name": "Test"}
        assert db_object.model_dump() == expected_dict
