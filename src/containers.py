from dependency_injector import containers, providers

from app.events.EventFactory import EventFactory
from app.events.EventsRegistry import EventsRegistry
from app.events.handlers.EventHandlerFactory import EventHandlerFactory


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.main"])

    events_registry = providers.Singleton(EventsRegistry)
    event_factory = providers.Factory(EventFactory, event_registry=events_registry)
    event_handler_factory = providers.Factory(EventHandlerFactory, event_registry=events_registry)

