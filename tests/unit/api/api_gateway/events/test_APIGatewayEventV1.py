import pytest

from api.api_gateway.events.APIGatewayEventV1 import APIGatewayEventV1
from unit.api.api_gateway.events.test_APIGatewayEventBase import TestAPIGatewayEventBase


class TestAPIGatewayEventV1(TestAPIGatewayEventBase):
    @pytest.fixture
    def event_dict(self):
        return {"resource": "/{proxy+}", "httpMethod": "POST", "requestContext": {"stage": "default"}}

    @pytest.fixture
    def event(self, event_dict, event_context) -> APIGatewayEventV1:
        return APIGatewayEventV1(event=event_dict, context=event_context)

    def test_init_event_v1(self, event):
        assert isinstance(event, APIGatewayEventV1)

    def test_get_body(self, event):
        assert event.get_body() == event.event

    def test_get_context(self, event):
        assert event.get_context() == event.context

    def test_get_stage(self, event, event_dict):
        assert event.get_stage() == event_dict.get("requestContext", {}).get("stage", "")

    def test_version(self, event):
        assert event.get_version() == "v1"
