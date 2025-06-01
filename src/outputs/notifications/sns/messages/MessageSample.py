import json

from inputs.sns.events.SNSEventSample import SNSEventSample
from outputs.notifications.interfaces.MessageI import MessageI


class MessageSample(MessageI):
    event_type: str
    sample_name: str

    def __init__(self, sample_name: str):
        self.event_type = SNSEventSample.get_event_type()
        self.sample_name = sample_name

    def __str__(self) -> str:
        return json.dumps({
            "type": self.event_type,
            "name": self.sample_name
        })