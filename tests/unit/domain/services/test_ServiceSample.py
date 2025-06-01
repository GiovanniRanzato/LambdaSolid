import datetime
from unittest.mock import MagicMock

from domain.models.ModelSample import ModelSample
from domain.services.ServiceSample import ServiceSample
import pytest

from outputs.db.interfaces.DBObjectI import DBObjectI
from outputs.db.interfaces.DBTableI import DBTableI


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

    @pytest.fixture
    def now(self):
        return datetime.datetime.now()

    @pytest.fixture
    def now_mock(self, mocker, now):
        mocker.patch('domain.services.ServiceSample.datetime', autospec=True)
        mocker.patch('domain.services.ServiceSample.datetime.now', return_value=now)
        return now

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

    def test_process_event_sample(self, service, sample_model, mocker, now_mock):
        sample_model_mock = mocker.patch('domain.services.ServiceSample.ModelSample', return_value=sample_model)

        service.create = MagicMock(return_value=sample_model)

        service.process_event_sample("sample_name")

        service.create.assert_called_once_with(sample_model)
        sample_model_mock.assert_called_once_with(
            name="sample_name",
            created_at=now_mock,
            updated_at=now_mock
        )