import pytest

from infrastructure.interfaces.EventI import EventI
from inputs.sns.events.SNSEventBase import SNSEventBase

class TestSNSEventBase:
    @pytest.fixture
    def sns_event_dict(self):
        return {
            "EventSource": "aws:sns",
            "Sns": {
                "Message": '{"type": "SNSEventBase"}',
            }
        }

    @pytest.fixture
    def sns_event_base(self, sns_event_dict):
        return SNSEventBase(
            event=sns_event_dict
        )

    def test_init(self, sns_event_base, sns_event_dict):
        assert isinstance(sns_event_base, SNSEventBase)
        assert isinstance(sns_event_base, EventI)
        assert sns_event_base.event == sns_event_dict

    def test_get_event_type(self):
        assert SNSEventBase.get_event_type() == "SNSEventBase"

    def test_from_dict(self, sns_event_dict):
        event = SNSEventBase.from_dict(sns_event_dict, None)
        assert isinstance(event, SNSEventBase)
        assert event.event == sns_event_dict

    def test_fail_from_dict(self):
        with pytest.raises(ValueError):
            SNSEventBase.from_dict({}, None)

    def test_is_valid(self, sns_event_dict):
        assert SNSEventBase.is_valid(sns_event_dict) is True

    def test_not_valid_event(self):
        invalid_event = {
            "EventSource": "aws:sns",
            "Sns": {
                "Message": '{"type": "InvalidEventType"}'
            }
        }
        assert SNSEventBase.is_valid(invalid_event) is False


