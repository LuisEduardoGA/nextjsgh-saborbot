import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Carga las variables de entorno
# Asume que el archivo .env está en un directorio que Alembic puede ver
load_dotenv()

# Esto apunta al objeto metadata de SQLAlchemy, asegurando que Alembic
# sepa qué modelos debe rastrear.
from app.database import Base
from app.models import *

target_metadata = Base.metadata

load_dotenv()

# Configurar URL de la DB desde variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construye la URL de conexión con el driver psycopg2
ALEMBIC_DB_URL =f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# *************************************************************
# 3. Configuración estándar de Alembic
# *************************************************************
# Esto es necesario para leer el resto de la configuración de alembic.ini.
config = context.config

# Interpreta la configuración de logging de alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# La sección "main" de alembic.ini
section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST) # type: ignore


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = ALEMBIC_DB_URL # Usa la URL construida para modo offline
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
        url=ALEMBIC_DB_URL, # Pasa la URL construida al contexto
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True, # Importante para la autogeneración
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()