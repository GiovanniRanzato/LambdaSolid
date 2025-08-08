import pytest
from outputs.db.sql_db.serializers.SqlORMSerializer import SqlORMSerializer

class TestSqlORMSerializer:
    @pytest.fixture
    def sql_orm_serializer(self):
        return SqlORMSerializer()

    def test_to_db(self, sql_orm_serializer, mocker):
        db_object = mocker.Mock()
        db_object.model_dump.return_value = {"field1": "value1", "field2": "value2"}
        expected_result = mocker.Mock()

        orm_class = mocker.Mock()
        # Force the orm_class to return expected_result object when instantiated
        orm_class.return_value = expected_result

        result = sql_orm_serializer.to_db(db_object, orm_class)

        # Assert orm_instance has been instantiated with the correct attributes
        orm_class.assert_called_once_with(field1="value1", field2="value2")

        # Assert orm_instance is not None
        assert result == expected_result

    def test_from_db(self, sql_orm_serializer, mocker):
        orm_object = mocker.Mock()
        orm_object.__table__ = mocker.Mock()

        # Mock the columns of the ORM object
        col1 = mocker.Mock()
        col2 = mocker.Mock()
        col1.name = "field1"
        col2.name = "field2"
        orm_object.__table__.columns = [col1, col2]

        # Set the attributes of the ORM object
        orm_object.field1 = "value1"
        orm_object.field2 = "value2"

        # Mock the object_class to be instantiated
        object_class = mocker.Mock()
        expected_result = mocker.Mock()

        # Force the object_class to return expected_result object when instantiated
        object_class.return_value = expected_result

        result = sql_orm_serializer.from_db(orm_object, object_class)

        # Assert object_class has been instantiated with the correct attributes
        object_class.assert_called_once_with(field1="value1", field2="value2")

        # Assert result is the expected object
        assert result == expected_result


