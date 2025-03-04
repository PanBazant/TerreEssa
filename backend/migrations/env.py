import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Dodaj katalog backendu do sys.path, aby importy działały poprawnie
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import konfiguracji bazy danych i modeli
from database.database import Base, DATABASE_URL

# Pobranie konfiguracji Alembic
config = context.config

# Interpretacja pliku konfiguracyjnego Alembic dla logowania
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Rejestrowanie modeli dla autogeneracji migracji
target_metadata = Base.metadata

# Ustawienie URL bazy danych w pliku alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Uruchom migracje w trybie offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Uruchom migracje w trybie online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Wybór trybu migracji
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
