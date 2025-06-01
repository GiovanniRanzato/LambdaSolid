from unittest.mock import MagicMock

from domain.models.ModelSample import ModelSample
from domain.services.ServiceSample import ServiceSample
import pytest

from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBTableI import DBTableI


class TestServiceSample:
    @pytest.fixture
    def sample_db_table(self):
        return MagicMock(spec=DBTableI)

    @pytest.fixture
    def service(self, sample_db_table):
        return ServiceSample(sample_db_table=sample_db_table)

    @pytest.fixture
    def sample_model(self):
        sample = MagicMock(spec=ModelSample)
        return sample

    def test_init(self, service):
        assert isinstance(service, ServiceSample)

    def test_create(self, service, sample_db_table, sample_model):
        sample_db_table.create.return_value = sample_model

        result = service.create(sample=MagicMock(spec=DBObjectI))

        sample_db_table.create.assert_called_once()
        assert result == sample_model

    def test_create_type_error(self, service, sample_db_table):
        sample_db_table.create.return_value = "Not a ModelSample"

        with pytest.raises(TypeError):
            service.create(sample=MagicMock(spec=DBObjectI))

        sample_db_table.create.assert_called_once()
