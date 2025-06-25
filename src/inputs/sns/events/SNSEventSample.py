from inputs.sns.events.SNSEventBase import SNSEventBase
from inputs.sns.interfaces.SNSEventSampleI import SNSEventSampleI


class SNSEventSample(SNSEventBase, SNSEventSampleI):
    @classmethod
    def is_valid(cls, event: dict) -> bool:
        super().is_valid(event)
        params = cls._get_content(event)
        return params.get("name") is not None and isinstance(params.get("name"), str)

    def get_event_sample_name(self) -> str:
        return self._get_content(self.event).get("name")
