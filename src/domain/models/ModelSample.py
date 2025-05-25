from datetime import datetime

from pydantic import BaseModel

from domain.interfaces.ModelI import ModelI
from repositories.interfaces.DBObjectI import DBObjectI


class ModelSample(BaseModel, ModelI, DBObjectI):
    sample_id: str = None
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None
