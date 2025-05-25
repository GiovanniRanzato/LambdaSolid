from datetime import datetime

from pydantic import BaseModel

from domain.interfaces.ModelI import ModelI
from repositories.db.DBObjectBase import DBObjectBase


class ModelSample(DBObjectBase, BaseModel, ModelI):
    sample_id: str = None
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None
