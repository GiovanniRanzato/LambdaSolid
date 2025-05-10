import pytest

from infrastructure.App import App
from src import main


class TestMain:
    @pytest.fixture
    def event_dict(self):
        return {"some_key": "some_value"}

    @pytest.fixture
    def context_dict(self):
        return {"some_key": "some_value"}

    def test_lambda_handler(self, event_dict, context_dict, mocker):
        logging_error_mock = mocker.patch("logging.error")

        app_mock = mocker.Mock(spec=App)
        app_init_mock = mocker.patch("src.main.App", return_value=app_mock)

        main.lambda_handler(event_dict, context_dict)

        app_init_mock.assert_called_once()
        app_mock.run.assert_called_once_with(event_dict, context_dict)

        logging_error_mock.assert_not_called()

    def test_lambda_handler_error(self, event_dict, context_dict, mocker):
        logging_error_mock = mocker.patch("logging.error")

        app_mock = mocker.Mock(spec=App)
        app_mock.run.side_effect = Exception("An error occurred")
        mocker.patch("src.main.App", return_value=app_mock)

        main.lambda_handler(event_dict, context_dict)

        logging_error_mock.assert_has_calls([mocker.call("Error in lambda_handler: %s", "An error occurred")])
