from dependency_injector import containers, providers

from infrastructure.config.Config import Config
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.EventsRegistry import EventsRegistry
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.main"])
    config = providers.Singleton(Config)
    events_registry = providers.Singleton(EventsRegistry)
    event_factory = providers.Factory(EventFactory, events_registry=events_registry)

    dynamo_db_serializer = providers.Singleton(DynamoDBSerializer)
    sample_db_table = providers.Singleton(DynamoDBTableSample, config=config, serializer=dynamo_db_serializer)
