import pytest
from src import main

class TestMain:
    @pytest.fixture
    def api_gateway_event(self):
        return {
            'routeKey': 'some_value',
            'requestContext': {
                'accountId': 'some_value'
            }
        }

    @pytest.fixture
    def api_gateway_context(self):
        return None

    def test_api_gateway_event(self, api_gateway_event, api_gateway_context, mocker):
        logging_error_mock = mocker.patch('logging.error')
        main.lambda_handler(api_gateway_event, api_gateway_context)
        logging_error_mock.assert_not_called()

