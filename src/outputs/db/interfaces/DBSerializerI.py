from abc import ABC, abstractmethod

from outputs.db.interfaces.DBObjectI import DBObjectI


class DBSerializerI(ABC):
    @abstractmethod
    def to_db(self, db_object: DBObjectI) -> dict:
        """serialize to db"""

    @abstractmethod
    def from_db(self, data: dict, obj_class: type) -> DBObjectI:
        """deserialize from db"""
