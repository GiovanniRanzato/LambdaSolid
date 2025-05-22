from dataclasses import dataclass
from datetime import datetime

from repositories.interfaces.DBObjectI import DBObjectI

@dataclass
class SampleModel(DBObjectI):
    sample_id: str = None
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None

    def model_dump(self) -> dict:
        return self.__dict__