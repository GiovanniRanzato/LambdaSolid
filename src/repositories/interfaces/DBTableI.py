from abc import ABC, abstractmethod
from repositories.interfaces.DBObjectI import DBObjectI


class DBTableI(ABC):
    def __init__(self, db_config: dict):
        self.db_config = db_config

    @abstractmethod
    def save(self, db_object: DBObjectI) -> bool:
        """Saves the object to the database"""

    @abstractmethod
    def get(self, pk: str) -> DBObjectI | None:
        """Retrieves the object from the database using the partition key and value"""
