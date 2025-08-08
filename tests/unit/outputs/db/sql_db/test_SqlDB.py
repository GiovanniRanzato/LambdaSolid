from unittest.mock import MagicMock

import pytest

from infrastructure.interfaces.ConfigI import ConfigI
from outputs.db.sql_db.SqlDB import SqlDB


class TestSqlDB:
    @pytest.fixture()
    def sqlite_config(self) -> ConfigI:
        config = MagicMock(spec=ConfigI)
        config.get.side_effect = lambda key: {
            "SQL_DB_DRIVER": "sqlite",
            "SQLITE_DB_PATH": "sqlite_host",
        }.get(key, None)
        return config

    @pytest.fixture()
    def mysql_config(self) -> ConfigI:
        config = MagicMock(spec=ConfigI)
        config.get.side_effect = lambda key: {
            "SQL_DB_DRIVER": "mysql",
            "MY_SQL_DB_PATH": "TEST",
            "MY_SQL_DB_PORT": "TEST",
            "MY_SQL_DB_USER": "TEST",
            "MY_SQL_DB_PASSWORD": "TEST",
            "MY_SQL_DB_NAME": "TEST"
        }.get(key, None)
        return config

    @pytest.fixture
    def create_engine_mock(self, mocker):
        return mocker.patch("outputs.db.sql_db.SqlDB.create_engine", autospec=True)

    @pytest.fixture
    def sessionmaker_mock(self, mocker):
        return mocker.patch("outputs.db.sql_db.SqlDB.sessionmaker", autospec=True)

    @pytest.fixture
    def sqlite_db(self, sqlite_config, create_engine_mock, sessionmaker_mock):
        return SqlDB(config=sqlite_config)

    @pytest.fixture
    def mysql_db(self, mysql_config, create_engine_mock, sessionmaker_mock):
        return SqlDB(config=mysql_config)

    def test_init_sqlite(self, sqlite_db, sqlite_config, create_engine_mock, sessionmaker_mock):
        assert sqlite_db.config == sqlite_config
        engine = create_engine_mock.return_value
        create_engine_mock.assert_called_once()
        sessionmaker_mock.assert_called_once_with(bind=engine, future=True)

    def test_init_mysql(self, mysql_db, mysql_config, create_engine_mock, sessionmaker_mock):
        assert mysql_db.config == mysql_config
        engine = create_engine_mock.return_value
        create_engine_mock.assert_called_once()
        sessionmaker_mock.assert_called_once_with(bind=engine, future=True)

    def test_raise_error_for_unsupported_driver(self, create_engine_mock, sessionmaker_mock):
        config = MagicMock(spec=ConfigI)
        config.get.side_effect = lambda key: {
            "SQL_DB_DRIVER": "unsupported_driver"
        }.get(key, None)

        with pytest.raises(ValueError, match="Unsupported DB driver: unsupported_driver"):
            SqlDB(config=config)

        sessionmaker_mock.assert_not_called()
        create_engine_mock.assert_not_called()

