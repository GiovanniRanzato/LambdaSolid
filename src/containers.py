from dependency_injector import containers, providers

from app.events.EventFactory import EventFactory
from app.events.EventsRegistry import EventsRegistry
from app.handlers.HandlerFactory import HandlerFactory


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.main"])

    events_registry = providers.Singleton(EventsRegistry)
    event_factory = providers.Factory(EventFactory, events_registry=events_registry)
    handler_factory = providers.Factory(HandlerFactory, events_registry=events_registry)
