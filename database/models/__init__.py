from sqlalchemy.orm import registry

mapper_registry = registry()

import database.models.site  # noqa: E402
import database.models.push  # noqa: E402
import database.models.subscriber  # noqa: E402, F401

Base = mapper_registry.generate_base()  # noqa: E402, F401
