import pytest
from api.api_gateway.APIGatewayEvent import APIGatewayEvent


class TestAPIGatewayEvent:
    @pytest.fixture
    def event_dict(self):
        return {
            "routeKey": "test_route",
            "requestContext": "requestContext",
        }

    @pytest.fixture
    def event_context(self):
        return {
            "some_key": "some value",
        }

    @pytest.fixture
    def api_gateway_event(self, event_dict, event_context):
        return APIGatewayEvent(event=event_dict, context=event_context)

    def test_init(self, api_gateway_event, event_dict, event_context):
        assert isinstance(api_gateway_event, APIGatewayEvent)
        assert api_gateway_event.event == event_dict
        assert api_gateway_event.context == event_context

    def test_from_dict(self, event_dict, event_context):
        api_gateway_event = APIGatewayEvent.from_dict(event=event_dict, context=event_context)
        assert isinstance(api_gateway_event, APIGatewayEvent)
        assert api_gateway_event.event == event_dict
        assert api_gateway_event.context == event_context

    @pytest.mark.parametrize(
        "events,is_valid",
        [({"routeKey": "valid value", "requestContext": "valid value"}, True), ({"invalid": "invalid"}, False)],
    )
    def test_is_valid(self, events, is_valid):
        assert APIGatewayEvent.is_valid(events) is is_valid

    def test_get_event_type(self, api_gateway_event):
        assert api_gateway_event.get_event_type() == "APIGatewayEvent"

    def test_invalid_event(self):
        with pytest.raises(ValueError, match="Invalid event format for APIGatewayEvent: {'invalid_event': 'value'}"):
            APIGatewayEvent.from_dict(event={"invalid_event": "value"}, context={})
