import pytest

from infrastructure.interfaces.EventI import EventI
from inputs.sns.events.SNSEventSample import SNSEventSample


class TestSNSEventSample:
    @pytest.fixture
    def sns_event_dict(self):
        return {
            "EventSource": "aws:sns",
            "Sns": {
                "Message": '{"type": "SNSEventSample", "name": "SampleEvent"}',
            }
        }

    @pytest.fixture
    def sns_event_base(self, sns_event_dict):
        return SNSEventSample(
            event=sns_event_dict
        )

    def test_init(self, sns_event_base, sns_event_dict):
        assert isinstance(sns_event_base, SNSEventSample)
        assert isinstance(sns_event_base, EventI)
        assert sns_event_base.event == sns_event_dict

    def test_is_valid(self, sns_event_base):
        assert sns_event_base.is_valid(sns_event_base.event) is True

    def test_get_event_sample_name(self, sns_event_base):
        assert sns_event_base.get_event_sample_name() == 'SampleEvent'