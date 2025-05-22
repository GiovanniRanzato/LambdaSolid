import uuid
from dataclasses import dataclass

from datetime import datetime
import pytest

from repositories.db.DBObjectBase import DBObjectBase
from repositories.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer


@dataclass
class DummyFlatModel(DBObjectBase):
    id: str
    name: str
    datetime: datetime

@dataclass
class DummyNestedModel(DBObjectBase):
    id: str
    nested_prop: DummyFlatModel

@dataclass
class DummyNestedListModel(DBObjectBase):
    id: str
    nested_prop: list[DummyFlatModel]

@dataclass
class DummyNestedDict(DBObjectBase):
    id: str
    nested_prop: dict

@dataclass
class DummyNestedListStr(DBObjectBase):
    id: str
    nested_prop: list[str]

@dataclass
class DummyInvalidModel:
    id: str

@dataclass
class DummyNestedInvalidModel(DBObjectBase):
    id: str
    nested_prop: DummyInvalidModel


class TestDynamoDBSerializer:
    @pytest.fixture
    def serializer(self):
        return DynamoDBSerializer()

    @pytest.fixture
    def flat_model(self):
        return DummyFlatModel(id=uuid.uuid4().hex, name=uuid.uuid4().hex, datetime=datetime.now())

    @pytest.fixture
    def nested_model(self, flat_model):
        return DummyNestedModel(id=uuid.uuid4().hex, nested_prop=flat_model)

    @pytest.fixture
    def nested_list_model(self, flat_model):
        return DummyNestedListModel(id=uuid.uuid4().hex, nested_prop=[flat_model])

    @pytest.fixture
    def nested_dict(self, flat_model):
        return DummyNestedDict(id=uuid.uuid4().hex, nested_prop=flat_model.__dict__)

    @pytest.fixture
    def nested_list_str(self, flat_model):
        return DummyNestedListStr(id=uuid.uuid4().hex, nested_prop=[flat_model.name, flat_model.id])

    @pytest.fixture
    def invalid_model(self):
        return DummyInvalidModel(id=uuid.uuid4().hex)

    @pytest.fixture
    def nested_invalid_model(self, invalid_model):
        return DummyNestedInvalidModel(id=uuid.uuid4().hex, nested_prop=invalid_model)

    @pytest.fixture
    def flat_model_dict(self, flat_model):
        return {
            'id': flat_model.id,
            'name': flat_model.name,
            'datetime': flat_model.datetime.isoformat()
        }

    @pytest.fixture
    def nested_model_dict(self, nested_model):
        return {
            'id': nested_model.id,
            'nested_prop': {
                'id': nested_model.nested_prop.id,
                'name': nested_model.nested_prop.name,
                'datetime': nested_model.nested_prop.datetime
            }
        }

    @pytest.fixture
    def nested_dict_dict(self, nested_dict):
        return {
            'id': nested_dict.id,
            'nested_prop': {
                'id': nested_dict.nested_prop['id'],
                'name': nested_dict.nested_prop['name'],
                'datetime': nested_dict.nested_prop['datetime'].isoformat()
            }
        }

    @pytest.fixture
    def nested_list_model_dict(self, nested_list_model):
        return {
            'id': nested_list_model.id,
            'nested_prop': [
                {
                    'id': nested_list_model.nested_prop[0].id,
                    'name': nested_list_model.nested_prop[0].name,
                    'datetime': nested_list_model.nested_prop[0].datetime.isoformat()
                }
            ]
        }

    @pytest.fixture
    def nested_list_str_dict(self, nested_list_str):
        return {
            'id': nested_list_str.id,
            'nested_prop': nested_list_str.nested_prop
        }

    @pytest.fixture
    def nested_invalid_model_dict(self, nested_invalid_model):
        return {
            'id': nested_invalid_model.id,
            'nested_prop': nested_invalid_model.nested_prop.__dict__
        }

    def test_flat_model_serialization(self, serializer, flat_model):
        serialized = serializer.to_db(flat_model)
        assert isinstance(serialized, dict)
        assert serialized['id'] == flat_model.id
        assert serialized['name'] == flat_model.name


    def test_nested_model_serialization(self, serializer, nested_model):
        serialized = serializer.to_db(nested_model)
        assert isinstance(serialized, dict)
        assert serialized['id'] == nested_model.id
        assert serialized['nested_prop']['id'] == nested_model.nested_prop.id
        assert serialized['nested_prop']['name'] == nested_model.nested_prop.name
        assert serialized['nested_prop']['datetime'] == nested_model.nested_prop.datetime.isoformat()

    def test_nested_list_model_serialization(self, serializer, nested_list_model):
        serialized = serializer.to_db(nested_list_model)
        assert isinstance(serialized, dict)
        assert serialized['id'] == nested_list_model.id
        assert serialized['nested_prop'][0]['id'] == nested_list_model.nested_prop[0].id
        assert serialized['nested_prop'][0]['name'] == nested_list_model.nested_prop[0].name
        assert serialized['nested_prop'][0]['datetime'] == nested_list_model.nested_prop[0].datetime.isoformat()

    def test_nested_dict_serialization(self, serializer, nested_dict):
        serialized = serializer.to_db(nested_dict)
        assert isinstance(serialized, dict)
        assert serialized['id'] == nested_dict.id
        assert serialized['nested_prop']['id'] == nested_dict.nested_prop['id']
        assert serialized['nested_prop']['name'] == nested_dict.nested_prop['name']

    def test_nested_list_str_serialization(self, serializer, nested_list_str):
        serialized = serializer.to_db(nested_list_str)
        assert isinstance(serialized, dict)
        assert serialized['id'] == nested_list_str.id
        assert serialized['nested_prop'][0] == nested_list_str.nested_prop[0]
        assert serialized['nested_prop'][1] == nested_list_str.nested_prop[1]

    def test_flat_model_deserialization(self, serializer, flat_model_dict, flat_model):
        deserialized = serializer.from_db(flat_model_dict, DummyFlatModel)
        assert isinstance(deserialized, DummyFlatModel)
        assert deserialized == flat_model

    def test_nested_model_deserialization(self, serializer, nested_model_dict, nested_model):
        deserialized = serializer.from_db(nested_model_dict, DummyNestedModel)
        assert isinstance(deserialized, DummyNestedModel)
        assert deserialized == nested_model

    def test_nested_list_model_deserialization(self, serializer, nested_list_model_dict, nested_list_model):
        deserialized = serializer.from_db(nested_list_model_dict, DummyNestedListModel)
        assert isinstance(deserialized, DummyNestedListModel)
        assert deserialized == nested_list_model

    def test_nested_dict_deserialization(self, serializer, nested_dict, nested_dict_dict):
        deserialized = serializer.from_db(nested_dict_dict, DummyNestedDict)
        assert isinstance(deserialized, DummyNestedDict)
        assert deserialized == nested_dict

    def test_nested_list_str_deserialization(self, serializer, nested_list_str, nested_list_str_dict):
        deserialized = serializer.from_db(nested_list_str_dict, DummyNestedListStr)
        assert isinstance(deserialized, DummyNestedListStr)
        assert deserialized == nested_list_str

    def test_nested_invalid_model_serialization(self, serializer, nested_invalid_model):
        with pytest.raises(TypeError):
            test = serializer.to_db(nested_invalid_model)
            assert isinstance(test, dict)

    def test_nested_invalid_model_deserialization(self, serializer, nested_invalid_model_dict, nested_invalid_model):
        with pytest.raises(TypeError):
            serializer.from_db(nested_invalid_model_dict, DummyNestedInvalidModel)




