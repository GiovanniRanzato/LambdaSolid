from typing import Type

from domain.models import SampleModel
from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDB import DynamoDB

from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBSerializerI import DBSerializerI
from repositories.interfaces.DBTableI import DBTableI


class DynamoDBTableSample(DynamoDB, DBTableI):
    def __init__(self, config: ConfigI, serializer: DBSerializerI):

        super().__init__(config)
        self.table = self.resource.Table(config.get("DYNAMODB_SAMPLE_TABLE"))
        self.pk = config.get("DYNAMODB_SAMPLE_TABLE_PK")
        self.obj_class = Type[SampleModel]
        self.serializer = serializer

    def save(self, db_object: DBObjectI) -> bool:
        dynamo_dict = self.serializer.to_db(db_object)
        self.table.put_item(Item=dynamo_dict)
        return True

    def get(self, pk: str) -> DBObjectI | None:
        dynamo_dict = self.table.get_item(Key={self.pk: pk}).get('Item')
        if not dynamo_dict:
            return None
        return self.serializer.from_db(dynamo_dict, obj_class=self.obj_class)
