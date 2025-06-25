from infrastructure.interfaces.EventI import EventI
from inputs.event_bridge.events.EBEventBase import EBEventBase
import pytest


class TestEBEventBase:
    invalid_event_list = [
        "invalid type",
        {},
        {"invalid.key": ["arn:aws:events:rule/EBEventBase"]},
        {"source": "invalid.source"},
        {"source": "invalid.source", "resources": ["arn:aws:events:rule/AnotherEvent"]},
        {"source": "aws.events", "resources": ["arn:aws:sns:rule/InvalidEvent"]}
    ]

    @pytest.fixture
    def eb_event_base_dict(self):
        return {
            "source": "aws.events",
            "resources": [
                "arn:aws:events:rule/EBEventBase"
            ]
        }

    @pytest.fixture
    def eb_event_base(self, eb_event_base_dict):
        return EBEventBase(event=eb_event_base_dict)

    def test_init_eb_event_base(self, eb_event_base):
        assert isinstance(eb_event_base, EBEventBase)
        assert isinstance(eb_event_base, EventI)

    @pytest.mark.parametrize("invalid_event_dict", invalid_event_list )
    def test_init_with_invalid_event(self, invalid_event_dict):
        with pytest.raises(ValueError, match="Invalid event format for EBEventBase"):
            EBEventBase(event={})

    def test_is_valid(self, eb_event_base_dict):
        assert EBEventBase.is_valid(eb_event_base_dict) is True

    @pytest.mark.parametrize("invalid_event", invalid_event_list)
    def test_is_valid_with_invalid_event(self, invalid_event):
        invalid_event = {
            "source": "aws.sns",
            "resources": ["arn:aws:events:rule/EBEventBase"]
        }
        assert EBEventBase.is_valid(invalid_event) is False

    def test_from_dict(self, eb_event_base_dict):
        event = EBEventBase.from_dict(eb_event_base_dict, None)
        assert isinstance(event, EBEventBase)
        assert event.event == eb_event_base_dict

    def test_from_dict_with_not_valid_event(self):
        invalid_event = {
            "source": "aws.sns",
            "resources": ["arn:aws:sns:rule/EBEventBase"]
        }
        with pytest.raises(ValueError, match="Invalid event format for EBEventBase"):
            EBEventBase.from_dict(invalid_event, None)