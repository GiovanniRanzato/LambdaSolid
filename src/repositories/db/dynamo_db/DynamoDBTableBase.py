import uuid
from typing import Type

from infrastructure.interfaces.ConfigI import ConfigI
from repositories.db.dynamo_db.DynamoDB import DynamoDB

from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBSerializerI import DBSerializerI
from repositories.interfaces.DBTableI import DBTableI


class DynamoDBTableBase(DynamoDB, DBTableI):
    def __init__(self, table_name: str, pk: str, obj_class: Type[DBObjectI], serializer: DBSerializerI, config: ConfigI):
        super().__init__(config)

        self.table = self.resource.Table(table_name)
        self.pk = pk
        self.obj_class = obj_class
        self.serializer = serializer

    def create(self, db_object: DBObjectI) -> DBObjectI:
        setattr(db_object, self.pk, uuid.uuid4().hex)
        dynamo_dict = self.serializer.to_db(db_object)
        self.table.put_item(Item=dynamo_dict)
        return db_object

    def update(self, db_object: DBObjectI) -> DBObjectI:
        dynamo_dict = self.serializer.to_db(db_object)
        self.table.put_item(Item=dynamo_dict)
        return db_object

    def get(self, pk: str) -> DBObjectI | None:
        dynamo_dict = self.table.get_item(Key={self.pk: pk}).get("Item")
        if not dynamo_dict:
            return None
        return self.serializer.from_db(data=dynamo_dict, obj_class=self.obj_class)

    def delete(self, pk: str) -> bool:
        self.client.delete_item(
            TableName=self.table.name,
            Key={self.pk: {"S": pk}},
        )
        return True


