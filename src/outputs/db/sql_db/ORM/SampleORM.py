import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from outputs.db.sql_db.ORM.BaseORM import Base


class SampleORM(Base):
    __tablename__ = 'sample_table'
    sample_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

