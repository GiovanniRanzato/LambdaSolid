from repositories.interfaces.DBObjectI import DBObjectI


class DBObjectBase(DBObjectI):
    def model_dump(self) -> dict:
        return self.__dict__

