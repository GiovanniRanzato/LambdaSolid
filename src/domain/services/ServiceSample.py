from datetime import datetime

from domain.interfaces.ModelI import ModelI
from domain.models.ModelSample import ModelSample
from outputs.db.interfaces.DBTableI import DBTableI


class ServiceSample:
    def __init__(self, sample_db_table: DBTableI):
        self.sample_db_table = sample_db_table

    def create(self, sample: ModelSample) -> ModelI:
        created = self.sample_db_table.create(sample)
        if not isinstance(created, ModelI):
            raise TypeError(f"Expected ModelSample, got {type(created)}")
        return created

    def process_event_sample(self, sample_name: str) -> None:
        sample = ModelSample(name=sample_name, created_at=datetime.now(), updated_at=datetime.now())
        self.create(sample)
        print(f"Processed sample: {sample.model_dump_json()}")
