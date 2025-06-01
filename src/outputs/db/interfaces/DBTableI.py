from abc import ABC, abstractmethod

from outputs.db.interfaces.DBObjectI import DBObjectI


class DBTableI(ABC):
    @abstractmethod
    def create(self, db_object: DBObjectI) -> DBObjectI:
        """Creates a new object in the database"""

    @abstractmethod
    def update(self, db_object: DBObjectI) -> DBObjectI:
        """Updates an existing object in the database"""

    @abstractmethod
    def get(self, pk: str) -> DBObjectI | None:
        """Retrieves the object from the database using the partition key and value"""

    @abstractmethod
    def delete(self, pk: str) -> bool:
        """Deletes the object from the database using the partition key and value"""
