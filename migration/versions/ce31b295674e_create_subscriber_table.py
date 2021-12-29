"""create subscriber table

Revision ID: ce31b295674e
Revises: bfc7ca1c7a75
Create Date: 2021-12-28 07:19:39.071644

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'ce31b295674e'
down_revision = 'bfc7ca1c7a75'
branch_labels = None
depends_on = 'cd154eefba09'


def upgrade():
    op.create_table(
        "subscriber",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            unique=True,
        ),
        sa.Column("site_id", UUID(as_uuid=True), nullable=False),
        sa.Column("subscribed", sa.Boolean, nullable=False, default=True),
        sa.Column("push_endpoint", JSONB, nullable=False),
        sa.ForeignKeyConstraint(('site_id',), ['site.id'], name='subscriber_site_id_fk', ondelete='CASCADE',
                                onupdate='CASCADE'),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Index("subscriber_id_index", "id")
    )


def downgrade():
    op.drop_table("subscriber")
