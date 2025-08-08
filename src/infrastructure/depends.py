from domain.services.ServiceSample import ServiceSample
from infrastructure.EventsRegistry import EventsRegistry
from infrastructure.config.Config import Config
from infrastructure.factories.EventFactory import EventFactory
from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.dynamo_db.DynamoDBSerializer import DynamoDBSerializer
from outputs.db.dynamo_db.DynamoDBTableSample import DynamoDBTableSample
from outputs.db.interfaces.DBSerializerI import DBSerializerI
from outputs.db.interfaces.DBTableI import DBTableI
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI
from outputs.db.sql_db.serializers.SqlORMSerializer import SqlORMSerializer
from outputs.db.sql_db.tables.SqlDBTableSample import SqlDBTableSample


def get_config() -> ConfigI:
    return Config()


def get_events_registry() -> EventsRegistry:
    return EventsRegistry()


def get_events_factory() -> EventFactory:
    return EventFactory(events_registry=get_events_registry())


def get_dynamo_db_serializer() -> DBSerializerI:
    return DynamoDBSerializer()


def get_dynamo_db_table_sample() -> DBTableI:
    return DynamoDBTableSample(config=get_config(), serializer=get_dynamo_db_serializer())


def get_sql_db_serializer() -> SqlORMSerializerI:
    return SqlORMSerializer()


def get_sql_db_table_sample() -> DBTableI:
    return SqlDBTableSample(serializer=get_sql_db_serializer(), config=get_config())


def get_service_sample() -> ServiceSample:
    return ServiceSample(sample_db_table=get_dynamo_db_table_sample())

