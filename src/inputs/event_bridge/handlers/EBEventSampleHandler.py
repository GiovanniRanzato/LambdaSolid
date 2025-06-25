import logging

from dependency_injector.wiring import Provide

from domain.services.ServiceSample import ServiceSample
from infrastructure.containers import Container
from infrastructure.interfaces.HandlerI import HandlerI
from inputs.event_bridge.interfaces.EBEventSampleI import EBEventSampleI


class EBEventSampleHandler(HandlerI):
    def __init__(self, service_sample: ServiceSample = Provide[Container.service_sample]):
        self.service_sample = service_sample

    def handle(self, event: EBEventSampleI):
        logging.info("Start handling SNSEventSample")
        self.service_sample.process_event_sample(event.get_event_sample_name())
        logging.info("Finish handling SNSEventSample")
