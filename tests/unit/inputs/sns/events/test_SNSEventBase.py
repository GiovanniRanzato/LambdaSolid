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
            },
        }

    @pytest.fixture
    def sns_event_base(self, sns_event_dict):
        return SNSEventBase(event=sns_event_dict)

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

    def test_is_valid(self, sns_event_dict, mocker):
        super_mock = mocker.patch("inputs.sns.events.SNSEventBase.SNSEventBase.is_valid", return_value=True)
        assert SNSEventBase.is_valid(sns_event_dict) is True
        super_mock.assert_called_once_with(sns_event_dict)

    @pytest.mark.parametrize("invalid_event", [
        {},
        {"EventSource": "wrong_source"},
        {"WrongKey": "a value"},
        {"EventSource": "aws:sns", "Sns": {"Message": None}},
        {"EventSource": "aws:sns", "Sns": {}},
        {"EventSource": "aws:sns", "Sns": {"Message": '{"type": "AnotherType"}'}}
    ])
    def test_is_valid_with_invalid_event(self, invalid_event):
        assert SNSEventBase.is_valid(invalid_event) is False

    def test_not_valid_event(self):
        invalid_event = {"EventSource": "aws:sns", "Sns": {"Message": '{"type": "InvalidEventType"}'}}
        assert SNSEventBase.is_valid(invalid_event) is False
