from domain.models.ModelSample import ModelSample
from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.sql_db.ORM.SampleORM import SampleORM
from outputs.db.sql_db.interfaces.SqlORMSerializerI import SqlORMSerializerI
from outputs.db.sql_db.tables.SqlDBTableBase import SqlDBTableBase


class SqlDBTableSample(SqlDBTableBase):
    def __init__(self, serializer: SqlORMSerializerI, config: ConfigI):
        super().__init__(
            orm_class=SampleORM,
            obj_class=ModelSample,
            serializer=serializer,
            config=config)
