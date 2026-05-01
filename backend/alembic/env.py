from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.config import settings
from app.database import Base
from app import models  # IMPORTANT: import models
import os

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# --- NEW: handle test DB via -x db argument or env variable ---
x_arg_dict = context.get_x_argument(as_dictionary=True)
db_name = x_arg_dict.get("db") or os.getenv("DATABASE_URL_TEST_NAME") or settings.DB_NAME

# Build sync URL dynamically
database_url_sync = settings.database_url_sync.replace(settings.DB_NAME, db_name)


def run_migrations_offline():
    context.configure(
        url=database_url_sync,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": database_url_sync
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    