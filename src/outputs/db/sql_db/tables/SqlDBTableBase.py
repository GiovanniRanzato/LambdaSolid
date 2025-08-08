from typing import Type

from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.interfaces.DBObjectI import DBObjectI
from outputs.db.interfaces.DBTableI import DBTableI
from outputs.db.sql_db.ORM.BaseORM import Base
from outputs.db.sql_db.SqlDB import SqlDB
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI


class SqlDBTableBase(DBTableI, SqlDB):
    def __init__(
        self, orm_class: Type[Base],  obj_class: Type[DBObjectI], serializer: SqlORMSerializerI, config: ConfigI
    ):
        super().__init__(config)

        self.orm_class = orm_class
        self.obj_class = obj_class
        self.serializer = serializer

    def create(self, db_object: DBObjectI) -> DBObjectI:
        with self.session_local() as session:
            orm_obj = self.serializer.to_db(db_object, self.orm_class)
            session.add(orm_obj)
            session.commit()
            session.refresh(orm_obj)
            return self.serializer.from_db(orm_obj, self.obj_class)

    def update(self, db_object: DBObjectI) -> DBObjectI:
        with self.session_local() as session:
            orm_obj = self.serializer.to_db(db_object, self.orm_class)
            session.merge(orm_obj)  # merge fa insert o update
            session.commit()
            session.refresh(orm_obj)
            return self.serializer.from_db(orm_obj, self.obj_class)

    def get(self, pk: str) -> DBObjectI | None:
        with self.session_local() as session:
            orm_obj = session.get(self.orm_class, pk)
            if orm_obj is None:
                return None
            return self.serializer.from_db(orm_obj, self.obj_class)

    def delete(self, pk: str) -> bool:
        with self.session_local() as session:
            orm_obj = session.get(self.orm_class, pk)
            if orm_obj is None:
                return False
            session.delete(orm_obj)
            session.commit()
            return True

