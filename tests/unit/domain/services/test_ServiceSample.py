from unittest.mock import MagicMock
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
    def sample_data_dict(self):
        return {
            'sample_id': '123',
            'name': 'Test Sample',
        }

    def test_init(self, service):
        assert isinstance(service, ServiceSample)

    def test_create(self, service, sample_db_table, sample_data_dict):
        created_obj = MagicMock(spec=DBObjectI)
        sample_db_table.create.return_value = created_obj

        result = service.create(sample_data=sample_data_dict)

        sample_db_table.create.assert_called_once()
        assert result == created_obj

