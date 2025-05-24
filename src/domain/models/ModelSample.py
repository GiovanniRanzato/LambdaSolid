from dataclasses import dataclass
from datetime import datetime

from repositories.db.DBObjectBase import DBObjectBase


@dataclass
class ModelSample(DBObjectBase):
    sample_id: str = None
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None
