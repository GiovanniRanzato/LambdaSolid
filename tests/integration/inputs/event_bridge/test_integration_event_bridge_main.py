import pytest
from src import main


class TestMain:
    @pytest.fixture
    def eb_event(self):
        return {
            "source": "aws.events",
            "resources": ["arn:aws:events:rule/EBEventSample"],
            "detail": {"sample_name": "SampleEvent"},
        }

    def test_eb_event(self, eb_event, mocker):
        logging_error_mock = mocker.patch("logging.error")
        main.lambda_handler(eb_event, None)

        logging_error_mock.assert_not_called()
