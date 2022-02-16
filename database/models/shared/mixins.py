from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.sql import func


@dataclass
class BaseMixin:
    __sa_dataclass_metadata_key__ = "sa"

    created_at: datetime = field(
        init=False,
        metadata={
            "sa": sa.Column(sa.DateTime(timezone=True), server_default=func.now())
        },
    )

    updated_at: datetime = field(
        init=False,
        metadata={
            "sa": sa.Column(sa.DateTime(timezone=True), server_default=func.now())
        },
    )
