from domain.services.ServiceSample import ServiceSample
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.config.Config import Config
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer
from repositories.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from repositories.db.interfaces.DBSerializerI import DBSerializerI
from repositories.db.interfaces.DBTableI import DBTableI

def get_config() -> ConfigI:
    return Config()

def get_events_registry() -> EventsRegistry:
    return EventsRegistry()

def get_events_factory() -> EventFactory:
    return EventFactory(events_registry=get_events_registry())

def get_dynamo_db_serializer() -> DBSerializerI:
    return DynamoDBSerializer()

def get_db_table_sample() -> DBTableI:
    return DynamoDBTableSample(config=get_config(), serializer=get_dynamo_db_serializer())

def get_service_sample() -> ServiceSample:
    return ServiceSample(sample_db_table=get_db_table_sample())