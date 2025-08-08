from datetime import datetime
from outputs.db.sql_db.ORM.BaseORM import Base
from outputs.db.sql_db.ORM.SampleORM import SampleORM


class TestSampleORM:
    def test_init_sample_orm(self):
        sample_orm = SampleORM(
            sample_id="TestSampleID",
            name="Test Sample",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert isinstance(sample_orm, SampleORM)
        assert isinstance(sample_orm, Base)
        assert sample_orm.sample_id is not None
