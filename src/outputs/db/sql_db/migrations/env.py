from logging.config import fileConfig
import sys
import os

# Load environment variables from .env file
# WARNING: access to rootpath - this instruction can't handle directory structure changes if you move the file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src')))

# Alembic needs to be able to import the ORM models and other necessary modules.
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from outputs.db.sql_db.ORM.BaseORM import Base
from outputs.db.sql_db.ORM.SampleORM import SampleORM
target_metadata = Base.metadata

# Set up the database URL based on environment variables
driver = os.getenv("SQL_DB_DRIVER", "sqlite")

if driver == "mysql":
    user = os.getenv("MY_SQL_DB_USER")
    password = os.getenv("MY_SQL_DB_PASSWORD")
    host = os.getenv("MY_SQL_DB_HOST")
    port = os.getenv("MY_SQL_DB_PORT", "3306")
    db = os.getenv("MY_SQL_DB_NAME")
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
else:
    path = os.getenv("SQLITE_DB_PATH")
    db_url = f"sqlite:///{path}"

config.set_main_option("sqlalchemy.url", db_url)


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
