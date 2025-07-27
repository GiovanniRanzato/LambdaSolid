from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.interfaces.ConfigI import ConfigI


class SqlDB:
    def __init__(self, config: ConfigI):
        self.config = config

        db_url = self._build_connection_url()
        self.engine = create_engine(db_url, echo=True, future=True)
        self.session_local = sessionmaker(bind=self.engine, future=True)

    def _build_connection_url(self) -> str:
        db_driver = self.config.get("SQL_DB_DRIVER")

        if db_driver == "sqlite":
            db_path = self.config.get("SQLITE_DB_PATH")
            if db_path != ":memory:":
                project_root = Path(__file__).resolve().parents[4]  # es. src/outputs/db/sql_db -> root
                db_path = (project_root / db_path).resolve()

            return f"sqlite:///{db_path}"

        elif db_driver == "mysql":
            user = self.config.get("MY_SQL_DB_USER")
            password = self.config.get("MY_SQL_DB_PASSWORD")
            host = self.config.get("MY_SQL_DB_HOST")
            port = self.config.get("MY_SQL_DB_PORT")
            database = self.config.get("MY_SQL_DB_NAME")

            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        else:
            raise ValueError(f"Unsupported DB driver: {db_driver}")
