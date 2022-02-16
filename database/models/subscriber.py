import uuid
from database.models import mapper_registry
from database.models.shared.mixins import BaseMixin
from dataclasses import dataclass
from dataclasses import field

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression


@mapper_registry.mapped
@dataclass
class Subscriber(BaseMixin):
    __tablename__ = "subscriber"
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

    site_id: uuid.UUID = field(
        init=False,
        metadata={
            "sa": sa.Column(
                UUID(as_uuid=True),
                nullable=False,
            )
        },
    )

    subscription_info: JSONB = field(
        metadata={
            "sa": sa.Column(
                JSONB,
                nullable=False,
            )
        },
    )

    subscribed: bool = field(
        default=expression.true(),
        metadata={
            "sa": sa.Column(
                sa.BOOLEAN, nullable=False, server_default=expression.true()
            )
        },
    )

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ("site_id",),
            ["site.id"],
            name="subscriber_site_id_fk",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.Index("subscriber_id_index", "id"),
    )
