import pytest

from infrastructure.interfaces.EventI import EventI
from inputs.sns.events.SNSEventSample import SNSEventSample


class TestSNSEventSample:
    @pytest.fixture
    def sns_event_dict(self):
        return {
            "EventSource": "aws:sns",
            "Sns": {
                "Message": '{"type": "SNSEventSample"}'
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