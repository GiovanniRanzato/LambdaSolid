from domain.models.ModelSample import ModelSample
from repositories.interfaces.DBObjectI import DBObjectI
from repositories.interfaces.DBTableI import DBTableI


class ServiceSample:
    def __init__(self, sample_db_table: DBTableI):
        self.sample_db_table = sample_db_table

    def create(self, sample: ModelSample) -> DBObjectI:
        return self.sample_db_table.create(sample)
