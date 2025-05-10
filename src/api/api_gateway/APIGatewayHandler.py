from infrastructure.interfaces.EventI import EventI
from infrastructure.interfaces.HandlerI import HandlerI


class APIGatewayHandler(HandlerI):
    def handle(self, event: EventI):
        print(f"Handling API Gateway event: {event}")
