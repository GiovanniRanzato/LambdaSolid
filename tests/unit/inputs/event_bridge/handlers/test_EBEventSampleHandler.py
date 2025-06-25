from unittest.mock import MagicMock

import pytest

from infrastructure.interfaces.HandlerI import HandlerI
from inputs.event_bridge.handlers.EBEventSampleHandler import EBEventSampleHandler

from domain.services.ServiceSample import ServiceSample
from inputs.event_bridge.interfaces.EBEventSampleI import EBEventSampleI


class TestEBEventSampleHandler:
    @pytest.fixture
    def service_sample(self):
        return MagicMock(spec=ServiceSample)

    @pytest.fixture
    def eb_event_sample_handler(self, service_sample):
        return EBEventSampleHandler(service_sample=service_sample)

    @pytest.fixture
    def eb_event_sample(self, mocker):
        return mocker.MagicMock(spec=EBEventSampleI)

    def test_init(self, eb_event_sample_handler):
        assert isinstance(eb_event_sample_handler, EBEventSampleHandler)
        assert isinstance(eb_event_sample_handler, HandlerI)
        assert eb_event_sample_handler.service_sample is not None

    def test_handle(self, eb_event_sample_handler, service_sample, eb_event_sample):
        eb_event_sample.get_event_sample_name.return_value = "sample_name"
        eb_event_sample_handler.handle(eb_event_sample)
        service_sample.process_event_sample.assert_called_once_with("sample_name")