from pytest_alembic.tests import experimental
from pytest_alembic.tests import test_model_definitions_match_ddl  # noqa: F401
from pytest_alembic.tests import test_single_head_revision  # noqa: F401
from pytest_alembic.tests import test_up_down_consistency  # noqa: F401
from pytest_alembic.tests import test_upgrade  # noqa: F401


def test_all_models_register_on_metadata(alembic_runner):
    experimental.test_all_models_register_on_metadata(alembic_runner, "database.models")
