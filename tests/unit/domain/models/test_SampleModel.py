import datetime
import uuid

import pytest
from domain.models.ModelSample import ModelSample


class TestSampleModel:
    @pytest.fixture
    def sample_model(self):
        return ModelSample(
            sample_id=uuid.uuid4().hex,
            name=uuid.uuid4().hex,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

    def test_init(self, sample_model):
        assert isinstance(sample_model, ModelSample)

    def test_model_dump(self, sample_model):
        result = sample_model.model_dump()
        assert isinstance(result, dict)
        assert result["sample_id"] == sample_model.sample_id
        assert result["name"] == sample_model.name
        assert result["created_at"] == sample_model.created_at
        assert result["updated_at"] == sample_model.updated_at
