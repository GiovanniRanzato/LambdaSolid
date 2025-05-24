from domain.models.SampleModel import SampleModel
from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDBTableBase import DynamoDBTableBase
from repositories.interfaces.DBSerializerI import DBSerializerI


class DynamoDBTableSample(DynamoDBTableBase):
    def __init__(self, config: ConfigI, serializer: DBSerializerI):
        super().__init__(
            table_name=config.get("DYNAMODB_SAMPLE_TABLE"),
            pk=config.get("DYNAMODB_SAMPLE_TABLE_PK"),
            obj_class=SampleModel,
            serializer=serializer,
            config=config,
        )
