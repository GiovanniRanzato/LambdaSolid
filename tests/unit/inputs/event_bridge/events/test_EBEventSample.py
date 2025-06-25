from inputs.event_bridge.events.EBEventBase import EBEventBase
from inputs.event_bridge.events.EBEventSample import EBEventSample
import pytest

from inputs.event_bridge.interfaces.EBEventSampleI import EBEventSampleI


class TestEBEventSample:
    @pytest.fixture
    def eb_event_sample_dict(self):
        return {
            "source": "aws.events",
            "resources": ["arn:aws:events:rule/EBEventSample"],
            "detail": {"sample_name": "SampleEvent"},
        }

    @pytest.fixture
    def eb_event_sample(self, eb_event_sample_dict):
        return EBEventSample(event=eb_event_sample_dict)

    def test_init_eb_event_sample(self, eb_event_sample, mocker):
        assert isinstance(eb_event_sample, EBEventSample)
        assert isinstance(eb_event_sample, EBEventSampleI)
        assert isinstance(eb_event_sample, EBEventBase)

    def test_is_valid(self, eb_event_sample_dict, mocker):
        mock_super = mocker.patch.object(EBEventBase, "is_valid", return_value=True)
        assert EBEventSample.is_valid(eb_event_sample_dict) is True
        mock_super.assert_called_once_with(eb_event_sample_dict)

    @pytest.mark.parametrize(
        "invalid_event",
        [
            {"source": "aws.events", "resources": ["arn:aws:events:rule/EBEventBase"], "detail": "not a dict"},
            {
                "source": "aws.events",
                "resources": ["arn:aws:events:rule/EBEventBase"],
                "detail": {"wrong_key": "str_val"},
            },
            {"source": "aws.events", "resources": ["arn:aws:events:rule/EBEventBase"], "detail": {"sample_name": 123}},
        ],
    )
    def test_is_valid_with_invalid_event(self, invalid_event):
        invalid_event = {"source": "aws.sns", "resources": ["arn:aws:events:rule/EBEventBase"]}
        assert EBEventSample.is_valid(invalid_event) is False

    def test_get_event_sample_name(self, eb_event_sample):
        assert eb_event_sample.get_event_sample_name() == "SampleEvent"
