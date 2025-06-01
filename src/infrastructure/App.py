from dependency_injector import providers
from dependency_injector.wiring import inject, Provide

from infrastructure.factories.EventFactory import EventFactory
from infrastructure.EventsRegistry import EventsRegistry

from inputs.api_gateway.events.APIGatewayEventV1 import APIGatewayEventV1
from inputs.api_gateway.APIGatewayHandler import APIGatewayHandler
from infrastructure.containers import Container
from infrastructure.interfaces.HandlerI import HandlerI


class App:
    @inject
    def __init__(
        self,
        event_factory: EventFactory = Provide[Container.event_factory],
        events_registry: EventsRegistry = Provide[Container.events_registry],
    ):
        self.event_factory = event_factory
        self.events_registry = events_registry

        self._register_events()

    def _register_events(self):
        # Register events and relative handlers here:
        # Example:
        self.events_registry.register_event(APIGatewayEventV1, APIGatewayHandler)
        pass

    def run(self, event: dict, context: dict):
        parsed_event = self.event_factory.create_event(event, context)
        handler_class = self.events_registry.resolve_handler_class(parsed_event)

        Container().wire(modules=[handler_class.__module__])
        handler: HandlerI = providers.Factory(handler_class)()

        return handler.handle(event=parsed_event)
