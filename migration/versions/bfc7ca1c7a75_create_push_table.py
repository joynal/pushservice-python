"""create push table

Revision ID: bfc7ca1c7a75
Revises: cd154eefba09
Create Date: 2021-12-28 07:19:31.185757

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'bfc7ca1c7a75'
down_revision = 'cd154eefba09'
branch_labels = None
depends_on = 'cd154eefba09'

status = ("QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELED")
status_enum = ENUM(*status, name="push_status", create_type=False)


def upgrade():
    op.create_table(
        "push",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            unique=True,
        ),
        sa.Column("site_id", UUID(as_uuid=True), nullable=False),
        sa.Column("status", status_enum, nullable=False, server_default="QUEUED"),
        sa.Column("title", sa.TEXT, nullable=False),
        sa.Column("options", JSONB, nullable=False),
        sa.Column("launch_url", sa.TEXT, nullable=False),
        sa.Column("priority", sa.TEXT, server_default="normal"),
        sa.Column("time_to_live", sa.INTEGER, default=259200),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.ForeignKeyConstraint(('site_id',), ['site.id'], name='push_site_id_fk', ondelete='CASCADE',
                                onupdate='CASCADE'),
        sa.Index("push_id_index", "id"),
        sa.Index("push_site_id_index", "site_id"),
    )


def downgrade():
    op.drop_table("push")
