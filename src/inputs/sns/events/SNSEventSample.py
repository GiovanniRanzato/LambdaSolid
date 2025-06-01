import json
from inputs.sns.events.SNSEventBase import SNSEventBase
from inputs.sns.interfaces.SNSEventI import SNSEventI


class SNSEventSample(SNSEventBase, SNSEventI):
    def get_content(self) -> dict:
        return json.loads(self.event.get("Sns").get("Message"))
