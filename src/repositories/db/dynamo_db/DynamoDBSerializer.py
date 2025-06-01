from datetime import datetime
from typing import Dict, Any, get_args, get_origin

from repositories.db.interfaces.DBObjectI import DBObjectI
from repositories.db.interfaces.DBSerializerI import DBSerializerI


class DynamoDBSerializer(DBSerializerI):
    def to_db(self, db_object: DBObjectI) -> Dict[str, Any]:
        def convert(v):
            if isinstance(v, DBObjectI):
                return {k: convert(val) for k, val in v.model_dump().items()}
            if isinstance(v, list):
                return [convert(i) for i in v]
            if isinstance(v, dict):
                return {k: convert(val) for k, val in v.items()}
            if isinstance(v, datetime):
                return v.isoformat()
            if isinstance(v, (str, int, float, bool)):
                return v
            raise TypeError

        return {k: convert(v) for k, v in db_object.model_dump().items()}

    def from_db(self, data: Dict[str, Any], obj_class: DBObjectI) -> DBObjectI:
        annotations = getattr(obj_class, "__annotations__", {})

        def convert_field(k, v):
            field_type = annotations.get(k, type(v))
            origin = get_origin(field_type)

            # List of objects DBObjectI
            if origin is list:
                sub_type = get_args(field_type)[0]
                if isinstance(v, list) and issubclass_safe(sub_type, DBObjectI):
                    return [self.from_db(i, sub_type) if isinstance(i, dict) else i for i in v]
                return v

            # Dict
            if isinstance(v, dict):
                if issubclass_safe(field_type, DBObjectI):
                    return self.from_db(v, field_type)
                return {ik: convert_field(ik, iv) for ik, iv in v.items()}

            # datetime from ISO str
            if isinstance(v, str):
                try:
                    return datetime.fromisoformat(v)
                except ValueError:
                    return v

            return v

        def issubclass_safe(cls, base):
            try:
                return issubclass(cls, base)
            except TypeError:
                return False

        cleaned = {k: convert_field(k, v) for k, v in data.items()}
        return obj_class(**cleaned)
