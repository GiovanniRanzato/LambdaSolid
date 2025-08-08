from typing import Type

from outputs.db.interfaces.DBObjectI import DBObjectI
from outputs.db.sql_db.ORM.BaseORM import Base


class SqlORMSerializerI:
    def to_db(self, db_object: DBObjectI, orm_class: Type[Base]) -> Base:
        """Serialize to database format."""

    def from_db(self, orm_object: Base, object_class: Type[DBObjectI]) -> DBObjectI:
        """Deserialize from database format to object."""