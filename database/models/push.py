import uuid
from database.models import mapper_registry
from database.models.shared.enums import StatusEnum
from database.models.shared.mixins import BaseMixin
from dataclasses import dataclass
from dataclasses import field

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Enum as EnumColumn


@mapper_registry.mapped
@dataclass
class Push(BaseMixin):
    __tablename__ = "push"
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

    title: str = field(
        metadata={
            "sa": sa.Column(
                sa.TEXT,
                nullable=False,
            )
        },
    )

    options: JSONB = field(
        metadata={
            "sa": sa.Column(
                JSONB,
                nullable=False,
            )
        },
    )

    launch_url: str = field(
        metadata={
            "sa": sa.Column(
                sa.TEXT,
                nullable=False,
            )
        },
    )

    status: str = field(
        default="QUEUED",
        metadata={
            "sa": sa.Column(
                EnumColumn(StatusEnum, name="push_status_enum"),
                nullable=False,
                server_default="QUEUED",
            )
        },
    )

    priority: str = field(
        default="normal",
        metadata={
            "sa": sa.Column(
                sa.TEXT,
                server_default="normal",
            )
        },
    )

    time_to_live: int = field(
        default=259200,
        metadata={
            "sa": sa.Column(
                sa.INTEGER,
                server_default="259200",
            )
        },
    )

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ("site_id",),
            ["site.id"],
            name="push_site_id_fk",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.Index("push_id_index", "id"),
        sa.Index("push_site_id_index", "site_id"),
    )
