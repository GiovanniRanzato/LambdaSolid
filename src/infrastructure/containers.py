from dependency_injector import containers, providers

from domain.services.ServiceSample import ServiceSample
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

    db_serializer = providers.Singleton(DynamoDBSerializer)
    db_table_sample = providers.Singleton(DynamoDBTableSample, config=config, serializer=db_serializer)
    service_sample = providers.Factory(ServiceSample, sample_db_table=db_table_sample)
