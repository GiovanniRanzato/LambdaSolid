from api.api_gateway.events.APIGatewayEventBase import APIGatewayEventBase
from api.api_gateway.interfaces.APIGatewayRequestI import APIGatewayRequestI


class APIGatewayEventV1(APIGatewayRequestI, APIGatewayEventBase):
    def __init__(self, event: dict, context: dict | None):
        super().__init__(event, context)
        self.version = "v1"

    def get_body(self) -> dict:
        return self.event

    def get_context(self):
        return self.context

    def get_stage(self) -> str:
        return self.get_body().get("requestContext", {}).get("stage", "")

    def get_version(self) -> str:
        return self.version
