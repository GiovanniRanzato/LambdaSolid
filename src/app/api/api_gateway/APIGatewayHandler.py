from app.events.EventI import EventI
from app.handlers.HandlerI import HandlerI


class APIGatewayHandler(HandlerI):
    def handle(self, event: EventI):
        print(f"Handling API Gateway event: {event}")
