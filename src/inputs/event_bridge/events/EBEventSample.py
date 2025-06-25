from inputs.event_bridge.events.EBEventBase import EBEventBase
from inputs.event_bridge.interfaces.EBEventSampleI import EBEventSampleI


class EBEventSample(EBEventBase, EBEventSampleI):
    @classmethod
    def is_valid(cls, event: dict) -> bool:
        super().is_valid(event)

        detail = event.get('detail')
        return (
                isinstance(detail, dict) and
                isinstance(detail.get('sample_name'), str)
        )

    def get_event_sample_name(self):
        return self.event.get('detail').get('sample_name')



