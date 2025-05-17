from dependency_injector import containers, providers

from infrastructure.config.Config import Config
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.EventsRegistry import EventsRegistry


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.main"])
    config = providers.Singleton(Config)
    events_registry = providers.Singleton(EventsRegistry)
    event_factory = providers.Factory(EventFactory, events_registry=events_registry)
