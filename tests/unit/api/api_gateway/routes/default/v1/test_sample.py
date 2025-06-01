import datetime
import json
import uuid
from unittest.mock import MagicMock

import pytest
from inputs.api.api_gateway.routes.default.v1.sample import create
from domain.models.ModelSample import ModelSample


class TestSample:
    @pytest.fixture
    def service_sample(self):
        return MagicMock()

    @pytest.fixture
    def sample_model_generator(self):
        return lambda set_id: ModelSample(
            sample_id=uuid.uuid4().hex if set_id else None,
            name=uuid.uuid4().hex,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    @pytest.mark.asyncio
    async def test_it_should_health_check(self, sample_model_generator, service_sample):
        sample_model = sample_model_generator(set_id=False)
        created_service = sample_model_generator(set_id=True)

        service_sample.create.return_value = created_service

        result = await create(sample=sample_model, service_sample=service_sample)

        service_sample.create.assert_called_once_with(sample_model)
        assert result.status_code == 200

        body = json.loads(result.body)
        assert body == created_service.model_dump_json()

