from domain.models.ModelSample import ModelSample
from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.dynamo_db.DynamoDBTableBase import DynamoDBTableBase
from outputs.db.interfaces.DBSerializerI import DBSerializerI


class DynamoDBTableSample(DynamoDBTableBase):
    def __init__(self, config: ConfigI, serializer: DBSerializerI):
        super().__init__(
            table_name=config.get("DYNAMODB_SAMPLE_TABLE"),
            pk=config.get("DYNAMODB_SAMPLE_TABLE_PK"),
            obj_class=ModelSample,
            serializer=serializer,
            config=config,
        )
