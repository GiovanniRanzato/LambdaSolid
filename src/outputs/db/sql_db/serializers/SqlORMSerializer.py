from typing import Type
from outputs.db.interfaces.DBObjectI import DBObjectI
from outputs.db.sql_db.ORM.BaseORM import Base
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI


class SqlORMSerializer(SqlORMSerializerI):
    def to_db(self, db_object: DBObjectI, orm_class: Type[Base]) -> Base:
        object_dict = db_object.model_dump()
        return orm_class(**object_dict)

    def from_db(self, orm_object: Base, object_class: Type[DBObjectI]) -> DBObjectI:
        object_attributes = {col.name: getattr(orm_object, col.name) for col in orm_object.__table__.columns}
        return object_class(**object_attributes)  # type: ignore[call-arg]