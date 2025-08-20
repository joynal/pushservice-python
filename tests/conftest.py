import os
import sys
from os.path import dirname

import pytest
import sqlalchemy

sys.path.insert(0, dirname(dirname(__file__)))

from pushservice.settings import load_settings  # noqa: E402
from pushservice.settings import Settings  # noqa: E402


@pytest.fixture
def alembic_config():
    """
    Override this fixture to configure the exact
    alembic context setup required.
    """
    config = {"script_location": "database/migration"}
    return config


@pytest.fixture
def alembic_engine():
    """
    Override this fixture to provide pytest-alembic powered
    tests with a database handle.
    """
    if os.getenv("RUNNING_CI", False):
        ci_db_settings = {
            "user": os.getenv("POSTGRES_USER", None),
            "password": os.getenv("POSTGRES_PASSWORD", None),
            "host": os.getenv("POSTGRES_HOST", None),
            "port": 5432,
            "database": os.getenv("POSTGRES_DB", None),
        }
        settings: Settings = Settings(**ci_db_settings)
    else:
        settings: Settings = load_settings("./settings.yaml")

    url = settings.database.connection_string.replace("postgres://", "postgresql://", 1)
    return sqlalchemy.create_engine(url)
