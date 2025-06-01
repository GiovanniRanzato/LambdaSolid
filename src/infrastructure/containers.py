from dependency_injector import containers, providers

from infrastructure.depends import get_config, get_events_registry
from infrastructure.factories.EventFactory import EventFactory


class Container(containers.DeclarativeContainer):
    wiring_modules = [
        "src.main",
        "src.inputs.api_gateway.routes.default.v1.sample",
    ]

    wiring_config = containers.WiringConfiguration(modules=wiring_modules)

    config = providers.Singleton(lambda: get_config())
    events_registry = providers.Singleton(lambda: get_events_registry())
    event_factory = providers.Factory(EventFactory, events_registry=events_registry)
