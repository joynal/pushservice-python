import uuid
from database.models import mapper_registry
from database.models.shared.mixins import BaseMixin
from dataclasses import dataclass
from dataclasses import field

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


@mapper_registry.mapped
@dataclass
class Site(BaseMixin):
    __tablename__ = "site"
    __sa_dataclass_metadata_key__ = "sa"

    id: uuid.UUID = field(
        init=False,
        metadata={
            "sa": sa.Column(
                UUID(as_uuid=True),
                primary_key=True,
                server_default=sa.text("gen_random_uuid()"),
                # unique=True,
            )
        },
    )

    public_key: str = field(
        metadata={
            "sa": sa.Column(
                sa.TEXT,
                nullable=False,
            )
        },
    )

    private_key: str = field(
        metadata={
            "sa": sa.Column(
                sa.TEXT,
                nullable=False,
            )
        },
    )

    __table_args__ = (sa.Index("site_id_index", "id"),)
