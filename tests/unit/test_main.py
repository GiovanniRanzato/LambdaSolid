import pytest

from src import main

class TestMain:
    @pytest.fixture
    def event_dict(self):
        return {
            'some_key': 'some_value'
        }
    @pytest.fixture
    def context_dict(self):
        return {
            'some_key': 'some_value'
        }

    def test_main(self, event_dict, context_dict, mocker):
        logging_mock = mocker.patch('logging.info')
        main.lambda_handler(event_dict, context_dict)
        logging_mock.assert_called_once_with("lambda_handler called")
