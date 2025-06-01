import pytest

from domain.services.ServiceSample import ServiceSample
from inputs.sns.handlers.SNSEventSampleHandler import SNSEventHandlerSample
from inputs.sns.interfaces.SNSEventSampleI import SNSEventSampleI


class TestSNSEventHandlerSample:
    @pytest.fixture
    def service_sample(self, mocker):
        return mocker.MagicMock(spec=ServiceSample)

    @pytest.fixture
    def sns_event_handler_sample(self, service_sample):
        return SNSEventHandlerSample(service_sample=service_sample)

    @pytest.fixture
    def sns_event_sample(self, mocker):
        return mocker.MagicMock(spec=SNSEventSampleI)

    def test_init(self, sns_event_handler_sample, service_sample):
        assert isinstance(sns_event_handler_sample, SNSEventHandlerSample)
        assert sns_event_handler_sample.service_sample == service_sample

    def test_handle(self, sns_event_handler_sample, service_sample, sns_event_sample, mocker):
        sns_event_sample.get_event_sample_name.return_value = "sample_name"

        sns_event_handler_sample.handle(sns_event_sample)

        service_sample.process_event_sample.assert_called_once_with("sample_name")
