import pytest

from outputs.notifications.interfaces.MessageI import MessageI
from outputs.notifications.sns.messages.MessageSample import MessageSample


class TestMessageSample:
    @pytest.fixture
    def message_sample(self):
        return MessageSample(sample_name="TestSample")

    def test_init(self, message_sample):
        assert isinstance(message_sample, MessageSample)
        assert isinstance(message_sample, MessageI)
        assert message_sample.sample_name == "TestSample"

    def test_str(self, message_sample):
        expected_str = '{"type": "SNSEventSample", "name": "TestSample"}'
        assert str(message_sample) == expected_str
        assert isinstance(str(message_sample), str)

