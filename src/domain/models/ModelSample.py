from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from domain.interfaces.ModelI import ModelI
from repositories.interfaces.DBObjectI import DBObjectI


class ModelSample(BaseModel, ModelI, DBObjectI):
    sample_id: Optional[str] = None
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
